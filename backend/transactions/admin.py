from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Transaction, TransactionItem


class TransactionItemInline(admin.TabularInline):
    """Inline admin for transaction items."""
    model = TransactionItem
    extra = 0
    readonly_fields = ['id', 'product', 'product_name', 'quantity', 'price', 'unit_price', 'points', 'matched', 'review_status']
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin interface for Transaction model."""

    list_display = ['id', 'user', 'store', 'total_points', 'scanned_at']
    list_filter = ['scanned_at', 'store']
    search_fields = ['id', 'user__email', 'store__name']
    ordering = ['-scanned_at']
    readonly_fields = ['id', 'user', 'store', 'total_points', 'receipt_url', 'receipt_data', 'scanned_at', 'created_at']
    inlines = [TransactionItemInline]

    fieldsets = (
        (None, {'fields': ('id', 'user', 'store', 'total_points')}),
        ('Receipt Info', {'fields': ('receipt_url', 'receipt_data')}),
        ('Timestamps', {'fields': ('scanned_at', 'created_at')}),
    )

    def has_add_permission(self, request):
        """Transactions are created via API only."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of transactions."""
        return False


@admin.register(TransactionItem)
class TransactionItemAdmin(admin.ModelAdmin):
    """Admin interface for TransactionItem model with review functionality."""

    list_display = ['product_name', 'transaction_user', 'quantity', 'price', 'unit_price', 'points', 'matched', 'review_status_badge', 'review_requested_at']
    list_filter = ['matched', 'review_status', 'review_requested_at']
    search_fields = ['transaction__id', 'product_name', 'product__name', 'transaction__user__email']
    ordering = ['-review_requested_at', '-transaction__scanned_at']
    readonly_fields = ['id', 'transaction', 'product', 'product_name', 'quantity', 'price', 'unit_price', 'matched', 'review_requested_at']
    actions = ['approve_reviews', 'reject_reviews']

    fieldsets = (
        (None, {'fields': ('id', 'transaction', 'product')}),
        ('Product Info', {'fields': ('product_name', 'quantity', 'price', 'unit_price')}),
        ('Points & Matching', {'fields': ('points', 'matched')}),
        ('Review Info', {'fields': ('review_status', 'review_requested_at', 'review_notes')}),
    )

    def transaction_user(self, obj):
        """Display user email from transaction."""
        return obj.transaction.user.email
    transaction_user.short_description = 'User'

    def review_status_badge(self, obj):
        """Display review status with color coding."""
        colors = {
            'none': 'gray',
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red',
        }
        color = colors.get(obj.review_status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_review_status_display()
        )
    review_status_badge.short_description = 'Review Status'

    def approve_reviews(self, request, queryset):
        """Approve selected reviews and assign default points."""
        from products.models import Product

        updated = 0
        for item in queryset.filter(review_status='pending'):
            # Create or get product in the database if not already linked
            if not item.product:
                product, created = Product.objects.get_or_create(
                    name=item.product_name,
                    defaults={
                        'description': f'Auto-created from approved review',
                        'points': 10,
                        'status': 'ACTIVE'
                    }
                )
                item.product = product

            # Assign default 10 points and mark as matched
            item.review_status = 'approved'
            item.matched = True
            item.points = 10
            item.review_notes = 'Approved by admin'
            item.save()

            # Update user points
            user = item.transaction.user
            user.points += 10
            user.save()

            # Update transaction total points
            transaction = item.transaction
            transaction.total_points += 10
            transaction.save()

            updated += 1

        self.message_user(request, f'{updated} review(s) approved. Products created and 10 points awarded per item.')
    approve_reviews.short_description = 'Approve selected reviews (10 points each)'

    def reject_reviews(self, request, queryset):
        """Reject selected reviews."""
        updated = queryset.filter(review_status='pending').update(
            review_status='rejected',
            review_notes='Rejected by admin'
        )
        self.message_user(request, f'{updated} review(s) rejected.')
    reject_reviews.short_description = 'Reject selected reviews'

    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('transaction__user', 'product')

    def has_add_permission(self, request):
        """Transaction items are created via API only."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of transaction items."""
        return False

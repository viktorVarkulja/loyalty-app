from django.contrib import admin
from .models import Transaction, TransactionItem


class TransactionItemInline(admin.TabularInline):
    """Inline admin for transaction items."""
    model = TransactionItem
    extra = 0
    readonly_fields = ['id', 'product', 'product_name', 'quantity', 'price', 'points', 'matched']
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
    """Admin interface for TransactionItem model."""

    list_display = ['transaction', 'product_name', 'quantity', 'price', 'points', 'matched']
    list_filter = ['matched']
    search_fields = ['transaction__id', 'product_name', 'product__name']
    ordering = ['-transaction__scanned_at']
    readonly_fields = ['id', 'transaction', 'product', 'product_name', 'quantity', 'price', 'points', 'matched']

    fieldsets = (
        (None, {'fields': ('id', 'transaction', 'product')}),
        ('Product Info', {'fields': ('product_name', 'quantity', 'price')}),
        ('Points', {'fields': ('points', 'matched')}),
    )

    def has_add_permission(self, request):
        """Transaction items are created via API only."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of transaction items."""
        return False

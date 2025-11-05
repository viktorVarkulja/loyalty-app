from django.contrib import admin
from django.utils import timezone
from .models import ReviewRequest


@admin.register(ReviewRequest)
class ReviewRequestAdmin(admin.ModelAdmin):
    """Admin interface for ReviewRequest model."""

    list_display = ['product_name', 'user', 'status', 'points_awarded', 'created_at', 'reviewed_at']
    list_filter = ['status', 'created_at', 'reviewed_at']
    search_fields = ['product_name', 'user__email', 'id']
    ordering = ['-created_at']
    readonly_fields = ['id', 'user', 'created_at', 'updated_at']

    fieldsets = (
        (None, {'fields': ('id', 'user', 'product_name', 'status')}),
        ('Receipt Data', {'fields': ('receipt_data',)}),
        ('Admin Action', {'fields': ('admin_comment', 'points_awarded')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'reviewed_at')}),
    )

    actions = ['approve_selected', 'reject_selected']

    def approve_selected(self, request, queryset):
        """Bulk approve review requests."""
        pending_requests = queryset.filter(status='PENDING')
        count = 0

        for review_request in pending_requests:
            review_request.status = 'APPROVED'
            review_request.reviewed_at = timezone.now()
            review_request.save()
            count += 1

        self.message_user(request, f'{count} review request(s) approved.')

    approve_selected.short_description = "Approve selected review requests"

    def reject_selected(self, request, queryset):
        """Bulk reject review requests."""
        pending_requests = queryset.filter(status='PENDING')
        count = 0

        for review_request in pending_requests:
            review_request.status = 'REJECTED'
            review_request.reviewed_at = timezone.now()
            review_request.save()
            count += 1

        self.message_user(request, f'{count} review request(s) rejected.')

    reject_selected.short_description = "Reject selected review requests"

    def save_model(self, request, obj, form, change):
        """Auto-set reviewed_at when status changes."""
        if change and 'status' in form.changed_data:
            if obj.status in ['APPROVED', 'REJECTED']:
                obj.reviewed_at = timezone.now()

                # Award points if approved
                if obj.status == 'APPROVED' and obj.points_awarded > 0:
                    user = obj.user
                    user.points += obj.points_awarded
                    user.save()

        super().save_model(request, obj, form, change)

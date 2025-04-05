from django.contrib import admin
from .models import UploadedDocument, UserProfile, CreditRequest

admin.site.register(UploadedDocument)

@admin.register(CreditRequest)
class CreditRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'timestamp', 'accept_request', 'reject_request')

    def accept_request(self, obj):
        return f'<a class="button" href="/admin/accept_request/{obj.id}/">✅ Accept</a>'
    accept_request.allow_tags = True
    accept_request.short_description = 'Accept'

    def reject_request(self, obj):
        return f'<a class="button" href="/admin/reject_request/{obj.id}/">❌ Reject</a>'
    reject_request.allow_tags = True
    reject_request.short_description = 'Reject'
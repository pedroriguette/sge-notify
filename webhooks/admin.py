from django.contrib import admin
from webhooks.models import WebHook


@admin.register(WebHook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_type', 'event')
    list_filter = ('event_type',)

from django.contrib import admin
from django.utils.html import format_html

from .models import RegisteredEmail, Support


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_filter = ['status']
    list_display = ['person', 'email', 'subject', 'created', 'status', '_']
    search_fields = ['person', 'email', 'subject']
    list_per_page = 10

    def _(self, obj):
        """
        Function to change the icons (Done/Pending)
        """
        if obj.status == obj.DONE:
            return True
        else:
            return False
    _.boolean = True

    def status(self, obj):
        """
        Function to color the status text.
        """
        if obj.status == obj.DONE:
            color = '#28a745'
        else:
            color = 'red'
        return format_html(f"<strong><p style='color: {color}'>{obj.status}</p></strong>")
    status.allow_tags = True

admin.site.register(RegisteredEmail)

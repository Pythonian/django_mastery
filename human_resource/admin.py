from django.contrib import admin

from .models import RegisteredEmail, Support, Message, Vacancy


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_filter = ['status']
    list_display = ['person', 'email', 'subject', 'created', 'status']
    search_fields = ['person', 'email', 'subject']
    list_per_page = 10


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'phone', 'email', 'subject', 'body']
    list_display = ['name', 'email', 'subject', 'report']
    list_filter = ['status']


admin.site.register(RegisteredEmail)
admin.site.register(Vacancy)

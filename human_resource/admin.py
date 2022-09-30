from django.contrib import admin
from django.utils.html import format_html

from .forms import CandidateForm
from .models import RegisteredEmail, Support, Message, Vacancy, Candidate


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'phone', 'email', 'subject', 'body']
    list_display = ['name', 'email', 'subject', 'report', 'status', '_']
    list_filter = ['status']

    def _(self, obj):
        if obj.status == 'R':
            return True
        else:
            return False
    _.boolean = True

    def status(self, obj):
        if obj.status == 'R':
            color = '#28a845'
        else:
            color = 'red'
        return format_html('<strong><p style="color: {}">{}</p></strong>'.format(color, obj.status))
    status.allow_tags = True


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    readonly_fields = ['firstname', 'lastname', 'email', 'job', 'created', 'salary',
                       'experience', 'birth_date', 'phonenumber', 'message', 'file', 'personality',
                       'smoker', 'libraries', 'databases', 'frameworks', 'mobile',
                       'gender', 'others', 'languages',
                       'institution', 'course', 'started_course', 'finished_course', 'course_description', 'course_status', 'company', 'position', 'started_job', 'finished_job', 'about_job', 'employed', 'remote', 'travel']
    list_display = ['__str__', 'email', 'job', 'created', 'job_status', '_']
    search_fields = ['firstname', 'lastname', 'email', 'status']
    list_filter = ['status']
    list_per_page = 10
    fieldsets = [
        ('HR Operations', {'fields': ['status', 'note']}),
        ('Personal', {'fields': ['experience', 'gender', 'job', 'email', 'phonenumber', 'salary', 'birth_date', 'personality', 'smoker', 'file', 'image', 'message']}),
        ('Skills', {'fields': ['frameworks', 'languages', 'libraries', 'databases', 'mobile', 'others']}),
        ('Education', {'fields': ['course_status', 'started_course', 'finished_course', 'institution', 'course', 'course_description']}),
        ('Profession', {'fields': ['started_job', 'finished_job', 'about_job']}),
        ('Note', {'fields': ['employed', 'remote', 'travel']})
    ]

    def get_fields(self, request, obj=None):
        """Exclude the firstname and lastname from admin display"""
        fields = super().get_fields(request, obj)
        if obj:
            fields.remove('firstname')
            fields.remove('lastname')
        return fields

    def _(self, obj):
        if obj.status == 'A':
            return True
        elif obj.status == 'P':
            return None
        else:
            return False
    _.boolean = True

    def job_status(self, obj):
        if obj.status == 'A':
            color = '#28a745'
        elif obj.status == 'P':
            color = '#fea95e'
        else:
            color = 'red'
        return format_html('<strong><p style="color: {}">{}</p></strong>'.format(color, obj.get_status_display()))
    job_status.allow_tags = True


admin.site.register(RegisteredEmail)
admin.site.register(Vacancy)
admin.site.register(Support)

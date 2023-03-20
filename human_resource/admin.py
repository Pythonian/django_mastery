from django.contrib import admin
from django.utils.html import format_html

from .models import Candidate, RegisteredEmail, Support, Message, Vacancy


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'phone', 'email', 'subject', 'body']
    list_display = ['name', 'email', 'subject', 'status']
    list_filter = ['status']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    readonly_fields = ['firstname', 'lastname', 'email', 'job', 'created', 'salary',
                       'experience', 'birth_date', 'phonenumber', 'message', 'file', 'personality',
                       'smoker', 'libraries', 'databases', 'frameworks', 'mobile',
                       'gender', 'others', 'languages',
                       'institution', 'course', 'started_course', 'finished_course', 'course_description', 'course_status', 'company', 'position', 'started_job', 'finished_job', 'about_job', 'employed', 'remote', 'travel']
    list_display = ['__str__', 'email', 'job', 'created', 'job_status', '_']
    search_fields = ['firstname', 'lastname', 'email', 'status']
    list_per_page = 10
    fieldsets = [
        ('HR Operations', {'fields': ['status', 'note']}),
        ('Personal', {'fields': ['experience', 'gender', 'job', 'email', 'phonenumber',
                                 'salary', 'birth_date', 'personality', 'smoker', 'file', 'image', 'message']}),
        ('Skills', {'fields': ['frameworks', 'languages',
                               'libraries', 'databases', 'mobile', 'others']}),
        ('Education', {'fields': ['course_status', 'started_course',
                                  'finished_course', 'institution', 'course', 'course_description']}),
        ('Profession', {'fields': [
         'started_job', 'finished_job', 'about_job']}),
        ('Note', {'fields': ['employed', 'remote', 'travel']})
    ]

    def change_view(self, request, object_id, extra_context=None):
        """ Override the page admin is directed to after saving a candidate."""
        result = super().change_view(request, object_id, extra_context)
        candidate = Candidate.objects.get(id__iexact=object_id)
        if not request.POST.__contains__('_addanother') and not request.POST.__contains__('_continue'):
            result['Location'] = candidate.get_absolute_url()
        return result

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

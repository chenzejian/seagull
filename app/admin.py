from django.forms import ModelForm, TextInput
from django.contrib.admin import ModelAdmin
from .models import Email, Project
from django.contrib import admin
from suit.widgets import (
    NumberInput, EnclosedInput, AutosizedTextarea,
    SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget
)
from django.core.urlresolvers import reverse


def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


class EmailForm(ModelForm):
    class Meta:
        widgets = {
            'title': TextInput(attrs={'class': 'input-mini'}),
            'send_times': NumberInput(attrs={'class': 'input-mini'}),
            'content': AutosizedTextarea(attrs={'rows': 3, 'class': 'input-xlarge'}),
            'created_at': SuitSplitDateTimeWidget,
            'updated_at': SuitSplitDateTimeWidget,
            # 'retry_times': EnclosedInput(append='次'),
        }

class EmailAdmin(admin.ModelAdmin):
    form = EmailForm
    fields = ['title', 'send_times', 'content']
    list_display = [
        'project_name',
        'title',
        'html_content',
        'send_times',
        'task_link',
        'status',
        # 'traceback',
        'created_at',
        'updated_at'
    ]
    list_filter = (('project__name', custom_titled_filter('project_name')),)
    search_fields = ['title', 'content']
    
    def has_add_permission(self, request):
        return False

    def status(self, x):
        return x.task.status

    def traceback(self, x):
        return x.task.traceback

    def project_name(self, x):
        return x.project.name

    def task_link(self, x):
      return u'<a href="/django_celery_results/taskresult/%s/change/">%s</a>' % (x.task.id, x.task.task_id)
    task_link.allow_tags = True
    task_link.short_description = "task"

    def html_content(self, x):
      return u'<div>%s</div>' % (x.content)
    html_content.allow_tags = True
    html_content.short_description = "content"


class ProjectForm(ModelForm):
    class Meta:
        widgets = {
            'name': TextInput(),
        }

class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    fields = ['name', 'status']
    list_display = [
        'name',
        'client_id',
        'client_secret',
        'status',
        'creator'
    ]
    search_fields = ['name']

    def status(self, x):
        if x.status == 1:
            return '正常'
        else:
            return '停用'

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'creator', None) is None:
            obj.creator = request.user
        obj.save()

admin.site.register(Email, EmailAdmin)
admin.site.register(Project, ProjectAdmin)
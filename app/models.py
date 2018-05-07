from django.db import models
from django_celery_results.models import TaskResult
from lib import utils
from django.contrib.auth.models import User



class Project(models.Model):
    BLOCK = 0
    NORMAL = 1
    STATUS_CHOICES = (
        (BLOCK, '停用'),
        (NORMAL, '正常'),
    )

    name = models.CharField(max_length=100)
    client_id = models.CharField(max_length=16, default='')
    client_secret = models.CharField(max_length=32, default='')
    success_emails = models.IntegerField(default=0)
    fail_emails = models.IntegerField(default=0)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=NORMAL)
    creator = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.client_id:
            self.client_id = utils.random_generate_string(16)
            self.client_secret = utils.random_generate_string(32)
        super(Project, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'project'

# Create your models here.
class Email(models.Model):
    title = models.CharField(max_length=1024)
    content = models.TextField()
    send_times = models.IntegerField(default=0)
    task = models.OneToOneField(TaskResult, to_field='task_id', default='')
    project = models.ForeignKey(Project)
    send_type = models.SmallIntegerField(default=0)
    from_user = models.CharField(max_length=255, default='')
    receive_user = models.CharField(max_length=255, default='')
    cc_user = models.CharField(max_length=255, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    SEND_TYPE_NAME = {
        1: 'mailgun', # 基础层的邮件服务
        2: 'self_service', # 本机的邮件服务
        3: 'qqsmtp' # 这个要求from_user必须是qq邮箱
    }

    class Meta:
        managed = False
        db_table = 'email'


email_schema = {
    'title': {
        'required': True,
        'type': 'string',
    },
    'content': {
        'required': True,
        'type': 'string',
    },
    'client_id': {
        'required': True,
        'type': 'string',
    },
    'sign': {
        'required': True,
        'type': 'string',
    },
    'from_user': {
        'required': True,
        'type': 'string',
    },
    'receive_user': {
        'required': True,
        'type': 'string',
    },
    'cc_user': {
        'required': True,
        'type': 'string',
    },
    'send_type': {
        'required': True,
        'type': 'integer',
        'coerce': int, 
    },
}
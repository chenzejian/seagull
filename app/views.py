from django.shortcuts import render
import json
from django.http import HttpResponse
from . import tasks
from django.views.decorators.csrf import csrf_exempt
from .models import Email, Project, email_schema
from lib import utils
from functools import wraps
import time
from django.conf import settings


def check_assign(func):
    @wraps(func)
    def returned_wrapper(request, *args, **kwargs):
        params = request.POST
        if 'client_id' not in params or params['client_id'] == '':
            return utils.HttpJSONResponse({'c':-1,'m':'client_id is required'})
        project = Project.objects.values('client_secret').filter(
            client_id=params['client_id'],
            status=Project.NORMAL
        ).first()
        if project is None:
            return utils.HttpJSONResponse({'c':-1,'m':'Your project not exist or be blocked'})
        params = params.copy()
        params.pop('sign')
        sign = utils.get_assign(params, project['client_secret'])
        if sign != request.POST.get('sign'):
            return utils.HttpJSONResponse({'c':-1,'m':'sign error'})
        return func(request, *args, **kwargs)
    return returned_wrapper


@csrf_exempt
@check_assign
def send_email(request):
    params = utils.get_checked_request_params(
        request.POST,
        email_schema
    )
    if params.get('error'):
        return utils.ErrResp((-1, params.get('error')))
    project = Project.objects.get(client_id=params['client_id'])
    print(project.id)
    email = Email(
        title=params['title'],
        content=params['content'],
        from_user=params['from_user'] if 'from_user' in params else settings.DEFAULT_FROM_USER, 
        receive_user=params['receive_user'],
        cc_user=params['cc_user'] if 'cc_user' in params else '', 
        send_type=params['send_type'], 
        send_times=0,
        project=project,
        task_id=0
    )
    
    email.save()

    res = tasks.send_mail.delay(email.id)
    email.task_id = res.id
    email.save()

    return utils.HttpJSONResponse({'c':0})

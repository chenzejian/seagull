import traceback
import json
import random
from django.http import HttpResponse
import hashlib
from cerberus import Validator
import requests
from django.conf import settings

DATACHECK = Validator()

def get_assign(params, access_secret):
    """获取签名"""
    if not isinstance(params, dict):
        return
    key_list = sorted(params.keys())
    _sigstr = ''.join([(item + "=" + str(params[item])) for item in key_list])
    strs = _sigstr+access_secret
    return hashlib.md5(strs.encode()).hexdigest()


def HttpJSONResponse(js):
    return HttpResponse(json.dumps(js), content_type='application/json')


def random_generate_string(length):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(length):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


def get_checked_request_params(params, schema, list_fields=[], allow_unknown=False):
    """从request.GET获取信息, where条件 views中处理
    :param params: request.POST or request.GET
    :param pagination: 是否分页
    :return: (limit, offset, fields,
    limit int
    offset int
    where dict
    fields dict
    """
    common_schema = {
        'fields': {'required': False, 'type': 'string'},
        'p': {'required': False, 'type': 'integer', 'coerce': int},
        'n': {'required': False, 'type': 'integer', 'coerce': int},
    }

    # 处理数组和空字符串
    params = params.copy()
    empty_params = []
    for key in params:
        if not params[key]:
            empty_params.append(key)
        if key in list_fields:
            params[key] = params.getlist(key)
    if empty_params:
        for key in empty_params:
            params.pop(key)

    # 验证
    DATACHECK.allow_unknown = allow_unknown
    schema = dict(schema, **common_schema)
    v = DATACHECK.validate(document=params.dict(), schema=schema)
    if not v:
        return {'error': DATACHECK.errors}

    # fields处理
    fields = list(set([i for i in params.get('fields').split(',')])) \
        if params.get('fields') else None

    # 分页
    limit = int(params.get('n')) if params.get('n') else 20
    page = int(params.get('p')) if params.get('p') else 1
    offset = (page - 1) * limit
    extra = {'limit': limit, 'page': page, 'offset': offset, 'fields': fields}
    return dict(params.dict(), **extra)

def ErrResp(c, extra_arg={}, d=None):
    if len(c) == 2:
        # c = error_code, error_msg
        c, m = c
    elif len(c) == 3:
        # 需要额外传参, c = error_code, error_msg, ['arg1', 'arg2'],
        # extra_arg={'arg1': 'val1', 'arg2': 'val2'}
        c, m, a = c
        if set(a) != set(extra_arg.keys()):
            raise Exception("You need extra argument in ErrResp: ", a)
        m = m.format(**extra_arg)
    return HttpJSONResponse({
        'c': c,
        'm': m,
        'd': d
    }) if d else HttpJSONResponse({
        'c': c,
        'm': m
    })

def mailgun_send_email(subject, html, to, from_email):
    result = requests.post(
        settings.MAILGUN_MESSAGE_URL,
        auth=("api", settings.MAILGUN_API),
        data={"from": from_email,
              "to": to,
              "subject": subject,
              "html": html,
              "o:testmode": False,
              })
    if not result:
        return None
    return result.json()
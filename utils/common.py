import datetime
from main import models
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import hashlib
import base64
import json


def more_month():
    today = datetime.date.today()
    more = datetime.timedelta(days=30)
    more_month = today - more
    return more_month

def getMonth():
    month = datetime.datetime.now().month
    return month


def getYear():
    year = datetime.datetime.now().year
    return year


def getDay():
    # day = datetime.datetime.now().day
    day = datetime.datetime.today()
    print(day)
    return day


def getYesterday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    yesterday=today-oneday
    return (yesterday, today)

def Yesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


def zdrang():
    last_day = models.Machine.objects.order_by('-order_time')[0].order_time
    end = models.Order.objects.order_by('-transaction_time')[0].transaction_time
    oneday = datetime.timedelta(days=1)
    start = last_day + oneday
    return (start, end)


def getToday():
    today=datetime.date.today()
    oneday=datetime.timedelta(days=1)
    tomorrow=today+oneday
    return (today, tomorrow)


def getMouth():
    today = datetime.date.today()
    mouth = datetime.timedelta(days=30)
    last_mouth = today - mouth
    return (last_mouth, today)


def up_kd(kdh):
    """查快递"""
    kd_dic = ''
    if kdh:
        up_zt(kdh)


def zt_kd(kdh):
    company_id='51fcad0f4aa94a94a3d03fbac4c10883'
    digest_key='b0b266ca0188'
    kdh = f'[{kdh}]'
    url = 'https://japi.zto.com/traceInterfaceNewTraces'
    post_fields = {'company_id': company_id,'data':kdh,'msg_type':'NEW_TRACES'}

    str_to_digest = ''
    for key, value in post_fields.items():
      str_to_digest+=(key+'='+value+'&')
    str_to_digest = str_to_digest[:-1] + digest_key

    m = hashlib.md5()
    m.update(str_to_digest.encode("UTF-8"))

    data_digest=base64.b64encode(m.digest())

    request = Request(url, urlencode(post_fields).encode())
    request.add_header('x-companyid', company_id)
    request.add_header('x-datadigest', data_digest)
    json_res = urlopen(request).read().decode()
    json_res = json.loads(json_res)
    json_res = json_res.get('data')[0].get('traces')
    if json_res:
        json_res = json_res[-1]
        msg = f'最后物流时间:<br>{json_res.get("scanDate")}<br>最后物流动态:<br>{json_res.get("desc")}'
    else:
        msg = '当前快递暂无动态<br>' \
              '若送机时间大于当前三天请咨询打单人员询问快递最新情况'
    return msg


def up_zt(kdh):
    company_id='51fcad0f4aa94a94a3d03fbac4c10883'
    digest_key='b0b266ca0188'
    kdh = f'[{kdh}]'
    url = 'https://japi.zto.com/traceInterfaceNewTraces'
    post_fields = {'company_id': company_id,'data':kdh,'msg_type':'NEW_TRACES'}

    str_to_digest = ''
    for key, value in post_fields.items():
      str_to_digest+=(key+'='+value+'&')
    str_to_digest = str_to_digest[:-1] + digest_key

    m = hashlib.md5()
    m.update(str_to_digest.encode("UTF-8"))

    data_digest=base64.b64encode(m.digest())

    request = Request(url, urlencode(post_fields).encode())
    request.add_header('x-companyid',company_id)
    request.add_header('x-datadigest',data_digest)
    json_res = urlopen(request).read().decode()
    json_res = json.loads(json_res)
    print(json_res.get('data'))
    print(123)
    res_list = json_res.get('data')[0].get('traces')
    # for res in res_list:
    #     print(res)
    #     print(1)
    print(res_list)
    print(1234)
    return res_list

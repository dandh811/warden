from lib.waf import WAF_RULE
import re
import json
import datetime
from urllib.parse import urlparse
from loguru import logger
import socket


def check_waf(headers, content):
    for i in WAF_RULE:
        name, method, position, regex = i.split('|')
        if method == 'headers':
            if headers.get(position) is not None:
                if re.search(regex, str(headers.get(position))) is not None:
                    return name
        else:
            if re.search(regex, str(content)):
                return name
    return None


def check_ip_format(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False


class EnJson(json.JSONEncoder):
    """python 转 json字符串时候对时间格式单独处理：json.dumps(python数据, cls=EnJson)"""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def url_is_ip(url):
    netloc = urlparse(url).netloc.split(':')[0]
    res = bool(re.search('[a-z]', netloc))
    return not res


def update_scan_status(target, type):
    try:
        cur_scan_status = target.scanned
        if cur_scan_status == 'not' or cur_scan_status == 'no':
            target.scanned = type
        elif type not in cur_scan_status:
            target.scanned = cur_scan_status + ',' + type
        target.save()
    except Exception as e:
        logger.critical(e)


def web_is_online(url):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(3)
    try:
        sk.connect((url, 443))
        return True
    except Exception:
        return False
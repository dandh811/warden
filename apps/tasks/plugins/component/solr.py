import requests
from lib.wechat_notice import wechat
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

vuln = ['solr']


def check(ip, ports, apps):
    if verify(vuln, ports, apps):
        try:
            url = 'https://' + ip
            url = url + '/solr/'
            g = requests.get(url, headers=get_ua(), timeout=5, verify=False)
            if g.status_code is 200 and 'Solr Admin' in g.content and 'Dashboard' in g.content:
                return 'Apache Solr Admin leask'
        except Exception:
            pass

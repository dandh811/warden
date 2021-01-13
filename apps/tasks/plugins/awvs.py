from apps.assets.models import Risk
import urllib3
import requests
import json
import time
from django.conf import settings
import re
from lib.wechat_notice import wechat
from loguru import logger
import sys


urllib3.disable_warnings()

host = settings.AWVS_HOST
api_header = settings.AWVS_API_HEADER
filename = 'out/%s.xlsx' % time.strftime("%H:%M:%S", time.localtime(time.time()))
awvs_scan_rule = {
                "full": "11111111-1111-1111-1111-111111111111",
                "highrisk": "11111111-1111-1111-1111-111111111112",
                "XSS": "11111111-1111-1111-1111-111111111116",
                "SQL": "11111111-1111-1111-1111-111111111113",
                "Weakpass": "11111111-1111-1111-1111-111111111115",
                "crawlonly": "11111111-1111-1111-1111-111111111117"
            }


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']
    assets = kwargs['assets']
    denominator = len(webapps)
    molecular = 0
    for webapp in webapps:
        molecular += 1

        logger.info('-' * 75)
        logger.info('+ 扫描插件: awvs')
        subdomain = webapp.subdomain
        logger.info('+ %s 扫描url: %s' % ((time.strftime("%H:%M:%S", time.localtime(time.time()))), subdomain))
        try:
            if not webapp.use_awvs_scan:
                logger.info('* 该web被指定不扫描')
                continue
            if webapp.report:
                continue
            if not bool(re.search('[a-z]', subdomain.split(':')[1])) and webapp.port in ['80', '443']:
                logger.info('+ 跳过url是IP，并且端口是80、443')
                continue
            target_id = add_task(subdomain)
            scan_task(subdomain, target_id)
            result = get_scan_info(target_id)
            get_reports(result, webapp)
            delete_target()
        except Exception as e:
            logger.info('* %s' % e)
            pass
        if molecular == denominator:
            percent = 100.0
            logger.info('+ 当前进度: %s [%d/%d]'%(str(percent)+'%', molecular, denominator))
        else:
            percent = round(1.0 * molecular / denominator * 100, 2)
            logger.info('+ 当前进度 : %s [%d/%d]'%(str(percent)+'%', molecular, denominator))


def add_task(url):
    data = {"address": url, "description": url, "criticality": "10"}
    try:
        response = requests.post(host + "api/v1/targets", data=json.dumps(data), headers=api_header, timeout=30, verify=False)
        result = json.loads(response.content.decode('utf-8'))
        return result['target_id']
    except Exception as e:
        logger.info('* %s' % e)
        return


def scan_task(url, target_id):
    data = {'target_id': target_id, 'profile_id': awvs_scan_rule['highrisk'],
        'schedule': {'disable': False, 'start_date': None, 'time_sensitive': False}}
    try:
        response = requests.post(url=host + 'api/v1/scans', timeout=10, verify=False, headers=api_header, data=json.dumps(data))
        if response.status_code == 201:
            logger.info('+ %s awvs 已开始扫描' % (time.strftime("%H:%M:%S", time.localtime(time.time()))))
    except Exception as e:
        logger.info('* %s' % e)


def get_scan_info(target_id):
    try:
        response = requests.get(host + "api/v1/scans", headers=api_header, timeout=30, verify=False)
        results = json.loads(response.content.decode('utf-8'))
        for result in results['scans']:
            if result['target_id'] == target_id:
                return result
    except Exception as e:
        logger.info('* %s' % e)


def get_status(result):
    # 获取scan_id的扫描状况
    try:
        scan_id = result['scan_id']
        response = requests.get(host + "api/v1/scans/" + str(scan_id), headers=api_header, timeout=30, verify=False)
        result = json.loads(response.content.decode('utf-8'))
        status = result['current_session']['status']
        # 如果是completed 表示结束.可以生成报告
        if status == "completed":
            return "completed"
        else:
            return result['current_session']['status']
    except Exception as e:
        logger.info('* %s' % e)
        return


def get_reports(result, webapp):
    # 获取scan_id的扫描报告
    """
        11111111-1111-1111-1111-111111111111    Developer
        21111111-1111-1111-1111-111111111111    XML
        11111111-1111-1111-1111-111111111119    OWASP Top 10 2013
        11111111-1111-1111-1111-111111111112    Quick
    """
    url = result['target']['address']
    count = 0
    while True:
        time.sleep(10)
        res = get_status(result)
        if res == 'completed':
            scan_id = result['scan_id']
            target_id = result['target_id']
            data = {"template_id": "11111111-1111-1111-1111-111111111111",
                    "source": {"list_type": "scans", "id_list": [scan_id]}}
            try:
                response = requests.post(host + "api/v1/reports", data=json.dumps(data), headers=api_header, timeout=30,
                                         verify=False)
                scan_result = response.headers
                loc = scan_result['Location']
            except Exception as e:
                logger.info('* %s' % e)
                sys.exit()
            logger.info('+ %s 扫描完成，正在生成报告 ...' % (time.strftime("%H:%M:%S")))
            while True:
                time.sleep(3)
                try:
                    response = requests.get(host.strip('/') + loc, headers=api_header, timeout=30, verify=False)
                    res = json.loads(response.content.decode('utf-8'))
                    if res['download']:
                        break
                except Exception as e:
                    logger.info(e)
            logger.info('+ %s 报告生成完毕，下载中 ...' % (time.strftime("%H:%M:%S", time.localtime(time.time()))))
            try:
                report_download_url = res['download'][0]
                report_response = requests.get(host.strip('/') + report_download_url, headers=api_header, timeout=30, verify=False)
                report_path_ = '/files/reports/' + scan_id + '.html'
                logger.info('+ 报告存储路径: %s' % report_path_)

                report_path = settings.BASE_DIR + report_path_
                with open(report_path, 'wb') as f:
                    f.write(report_response.content)
            except Exception as e:
                logger.info('* %s' % e)
                sys.exit()
            webapp.report = report_path_

            try:
                response = requests.get(host + 'api/v1/vulnerabilities?q=severity:3', headers=api_header, timeout=30, verify=False)
                res = json.loads(response.content.decode('utf-8'))
                vul_names = []
                ignore_vuls = ['nginx Integer Overflow']
                for vul in res['vulnerabilities']:
                    if vul['target_id'] == target_id and vul['vt_name'] not in ignore_vuls:
                        vul_names.append(vul['vt_name'])

                if vul_names:
                    for vul_name in vul_names:
                        logger.info('--- %s' % vul_name)
                    desc = '\n'.join(vul_names)
                    risk = Risk.objects.update_or_create(target=webapp.subdomain, risk_type='awvs扫描漏洞', defaults={'desc': desc})
                    webapp.risk = risk[0]
                    title = 'awvs扫描漏洞'
                    content = desc
                    wechat.send_msg(title, content)
                else:
                    logger.info('+ 未发现高风险漏洞')

            except Exception as e:
                logger.info('* %s' % e)

            webapp.save()
            logger.info('+ %s 报告已保存' % (time.strftime("%H:%M:%S", time.localtime(time.time()))))
            break
        if res == 'aborted':
            break


def delete_target():
    # 删除scan_id的扫描
    try:
        response = requests.get(host + "/api/v1/targets", headers=api_header, timeout=30, verify=False)
        res = json.loads(response.content.decode('utf-8'))
        for target in res['targets']:
            response = requests.delete(host + "/api/v1/targets/" + target['target_id'], headers=api_header, timeout=30, verify=False)
            # 如果是204 表示删除成功
            if response.status_code == 200:
                logger.info('+ %s 扫描记录已删除' % (time.strftime("%H:%M:%S", time.localtime(time.time()))))
            else:
                logger.info(response.status_code)
                logger.info('+ %s 扫描记录删除失败' % (time.strftime("%H:%M:%S", time.localtime(time.time()))))
    except Exception as e:
        logger.info('* %s' % e)


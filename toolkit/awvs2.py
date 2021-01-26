import pymysql
import time
import urllib3
import requests
import json
from loguru import logger

urllib3.disable_warnings()

AWVS_HOST = 'https://127.0.0.1:13443/'
AWVS_API_KEY = '1986ad8c0a5b3df4d7028d5f3c06e936c3765f2f4a2f54908a90f20fa01c9e3cc'
AWVS_API_HEADER = {"X-Auth": AWVS_API_KEY, "content-type": "application/json"}

awvs_scan_rule = {
    "full": "11111111-1111-1111-1111-111111111111",
    "highrisk": "11111111-1111-1111-1111-111111111112",
    "XSS": "11111111-1111-1111-1111-111111111116",
    "SQL": "11111111-1111-1111-1111-111111111113",
    "Weakpass": "11111111-1111-1111-1111-111111111115",
    "crawlonly": "11111111-1111-1111-1111-111111111117"
}

logger.info('start')


def start(subdomain):
    target_id = add_task(subdomain)
    scan_task(subdomain, target_id)
    # result = get_scan_info(target_id)
    # get_reports(result, subdomain)
    # print(subdomain)


def add_task(url):
    data = {"address": url, "description": url, "criticality": "10"}
    try:
        response = requests.post(AWVS_HOST + "api/v1/targets", data=json.dumps(data), headers=AWVS_API_HEADER,
                                 timeout=30, verify=False)
        result = json.loads(response.content.decode('utf-8'))
        # logger.info(url + ' 已添加')
        return result['target_id']
    except Exception as e:
        logger.critical('* %s' % e)
        return


def scan_task(url, target_id):
    data = {'target_id': target_id, 'profile_id': awvs_scan_rule['highrisk'],
            'schedule': {'disable': False, 'start_date': None, 'time_sensitive': False}}
    try:
        response = requests.post(url=AWVS_HOST + 'api/v1/scans', timeout=10, verify=False, headers=AWVS_API_HEADER,
                                 data=json.dumps(data))
        if response.status_code == 201:
            logger.info('%s 已开启扫描' % url)
            db = pymysql.connect(host="81.70.89.72", user="root", password="Sihun2016812", database="blog")
            cursor = db.cursor()
            sql2 = "UPDATE webapps_webapp SET awvs_scanned = 'yes' where subdomain = '%s'" % (subdomain)

            cursor.execute(sql2)
            db.commit()
            db.close()
            # logger.info('数据库已更新')
    except Exception as e:
        logger.critical(e)


def get_scan_info(target_id):
    try:
        response = requests.get(AWVS_HOST + "api/v1/scans", headers=AWVS_API_HEADER, timeout=30, verify=False)
        results = json.loads(response.content.decode('utf-8'))
        logger.info(results['scans'])
        for result in results['scans']:
            if result['target_id'] == target_id:
                logger.info(target_id)
                return result
    except Exception as e:
        logger.critical('* %s' % e)
        return


def get_status(result):
    # 获取scan_id的扫描状况
    try:
        logger.info(result)
        scan_id = result['scan_id']
        response = requests.get(AWVS_HOST + "api/v1/scans/" + str(scan_id), headers=AWVS_API_HEADER, timeout=5, verify=False)
        result = json.loads(response.content.decode('utf-8'))
        status = result['current_session']['status']
        # 如果是completed 表示结束.可以生成报告
        if status == "completed":
            return "completed"
        else:
            return result['current_session']['status']
    except Exception as e:
        logger.critical('* %s' % e)
        return 'aborted'


def get_reports(result, subdomain):
    while True:
        time.sleep(15)
        res = get_status(result)
        if res == 'completed':
            logger.info(subdomain + ', scan completed')

            try:
                db = pymysql.connect(host="81.70.89.72", user="root", password="Sihun2016812", database="blog")
                cursor = db.cursor()
                sql2 = "UPDATE webapps_webapp SET awvs_scanned = 'yes' where subdomain = '%s'" % (subdomain)

                cursor.execute(sql2)
                db.commit()
                db.close()
            except Exception as e:
                logger.critical(e)
            break
        if res == 'aborted':
            break


def get_scans_running_count():
    try:
        response = requests.get(AWVS_HOST + "/api/v1/me/stats", headers=AWVS_API_HEADER, timeout=30, verify=False)
        results = json.loads(response.content.decode('utf-8'))
        count = results['scans_running_count']
        # logger.info('目前运行任务数：' + str(count))
        return count
    except Exception as e:
        logger.critical('* %s' % e)
        return 5


sql = "select subdomain, waf_or_cdn, awvs_scanned from webapps_webapp"
subdomains = []


try:
    db = pymysql.connect(host="81.70.89.72", user="root", password="Sihun2016812", database="blog")
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()

    for row in results:
        if row[1]:
            continue
        if row[2] == 'yes':
            continue
        subdomain = row[0]
        subdomains.append(subdomain)
    db.close()
except Exception as e:
    logger.critical(e)


jobs = len(subdomains)
count = 0
i = 0

while True:
    count = get_scans_running_count()
    if count < 1:
        subdomain = subdomains[i]
        start(subdomain)
        time.sleep(15)

        i += 1
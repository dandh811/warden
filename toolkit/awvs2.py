import pymysql
import time
import urllib3
import requests
import json
from multiprocessing.dummy import Pool as ThreadPool

urllib3.disable_warnings()

AWVS_HOST = 'https://127.0.0.1:3443/'
AWVS_API_KEY = '1986ad8c0a5b3df4d7028d5f3c06e936c1bbb3c20f5594781ac70c726f6236874'
AWVS_API_HEADER = {"X-Auth": AWVS_API_KEY, "content-type": "application/json"}

awvs_scan_rule = {
                "full": "11111111-1111-1111-1111-111111111111",
                "highrisk": "11111111-1111-1111-1111-111111111112",
                "XSS": "11111111-1111-1111-1111-111111111116",
                "SQL": "11111111-1111-1111-1111-111111111113",
                "Weakpass": "11111111-1111-1111-1111-111111111115",
                "crawlonly": "11111111-1111-1111-1111-111111111117"
            }

print('start')

db = pymysql.connect("81.70.89.72", "root", "Sihun2016812", "blog")
cursor = db.cursor()


def start(subdomain):
    target_id = add_task(subdomain)
    scan_task(subdomain, target_id)
    result = get_scan_info(target_id)
    get_reports(result, subdomain)


def add_task(url):
    data = {"address": url, "description": url, "criticality": "10"}
    try:
        response = requests.post(AWVS_HOST + "api/v1/targets", data=json.dumps(data), headers=AWVS_API_HEADER, timeout=30, verify=False)
        result = json.loads(response.content.decode('utf-8'))
        return result['target_id']
    except Exception as e:
        print('* %s' % e)
        return


def scan_task(url, target_id):
    data = {'target_id': target_id, 'profile_id': awvs_scan_rule['highrisk'],
        'schedule': {'disable': False, 'start_date': None, 'time_sensitive': False}}
    try:
        response = requests.post(url=AWVS_HOST + 'api/v1/scans', timeout=10, verify=False, headers=AWVS_API_HEADER, data=json.dumps(data))
        if response.status_code == 201:
            print('+ %s awvs 已开始扫描' % (time.strftime("%H:%M:%S", time.localtime(time.time()))))
    except Exception as e:
        print('* %s' % e)


def get_scan_info(target_id):
    try:
        response = requests.get(AWVS_HOST + "api/v1/scans", headers=AWVS_API_HEADER, timeout=30, verify=False)
        results = json.loads(response.content.decode('utf-8'))
        for result in results['scans']:
            if result['target_id'] == target_id:
                return result
    except Exception as e:
        print('* %s' % e)


def get_status(result):
    # 获取scan_id的扫描状况
    try:
        scan_id = result['scan_id']
        response = requests.get(AWVS_HOST + "api/v1/scans/" + str(scan_id), headers=AWVS_API_HEADER, timeout=30, verify=False)
        result = json.loads(response.content.decode('utf-8'))
        status = result['current_session']['status']
        # 如果是completed 表示结束.可以生成报告
        if status == "completed":
            return "completed"
        else:
            return result['current_session']['status']
    except Exception as e:
        print('* %s' % e)
        return


def get_reports(result, subdomain):
    # 获取scan_id的扫描报告
    """
        11111111-1111-1111-1111-111111111111    Developer
        21111111-1111-1111-1111-111111111111    XML
        11111111-1111-1111-1111-111111111119    OWASP Top 10 2013
        11111111-1111-1111-1111-111111111112    Quick
    """
    url = result['target']['address']
    while True:
        time.sleep(10)
        res = get_status(result)
        if res == 'completed':
            print('completed')
            sql2 = "UPDATE webapps_webapp SET awvs_scanned = 'yes' where subdomain = '%c'" % (subdomain)
            try:
                cursor.execute(sql2)
                db.commit()
            except:
                pass
            break
        if res == 'aborted':
            break


def delete_target():
    # 删除scan_id的扫描
    try:
        response = requests.get(AWVS_HOST + "/api/v1/targets", headers=AWVS_API_HEADER, timeout=30, verify=False)
        res = json.loads(response.content.decode('utf-8'))
        for target in res['targets']:
            response = requests.delete(AWVS_HOST + "/api/v1/targets/" + target['target_id'], headers=AWVS_API_HEADER, timeout=30, verify=False)
            # 如果是204 表示删除成功
            if response.status_code == 200:
                print('+ %s 扫描记录已删除' % (time.strftime("%H:%M:%S", time.localtime(time.time()))))
            else:
                print(response.status_code)
                print('+ %s 扫描记录删除失败' % (time.strftime("%H:%M:%S", time.localtime(time.time()))))
    except Exception as e:
        print('* %s' % e)


def get_scans_running_count():
    try:
        response = requests.get(AWVS_HOST + "/api/v1/me/stats", headers=AWVS_API_HEADER, timeout=30, verify=False)
        results = json.loads(response.content.decode('utf-8'))
        count = results['scans_running_count']
        return count
    except Exception as e:
        print('* %s' % e)


sql = "select subdomain, waf_or_cdn, awvs_scanned from webapps_webapp"
subdomains = []

try:
    cursor.execute(sql)
    results = cursor.fetchall()
    print(1)

    for row in results:
        if row[1]:
            continue
        if row[2] == 'yes':
            continue
        subdomain = row[0]
        subdomains.append(subdomain)
except Exception as e:
    print(e)

try:
    pool = ThreadPool(5)
    ips2 = pool.map(start, subdomains)

    pool.close()
    pool.join()
except Exception as e:
    print(e)

db.close()

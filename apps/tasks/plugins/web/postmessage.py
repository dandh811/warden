from apps.assets.models import Risk
from lib.wechat_notice import wechat
import requests
from lib.common import update_scan_status
import subprocess
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool
from django.conf import settings
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import time

plugin = 'postmessage'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']
    if policy == 'increase':
        webapps = webapps.exclude(scanned__icontains=plugin)

    if not webapps:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
        return

    for webapp in webapps:
        check(webapp)
    # try:
    #     pool = ThreadPool(15)
    #     pool.map(check, webapps)
    #     pool.close()
    #     pool.join()
    # except Exception as e:
    #     pass


def check(webapp):
    url = webapp.subdomain
    # logger.debug("[%s] [%s] %s" % (plugin, webapp.id, url))

    try:
        r = requests.get(url, timeout=10, headers=settings.HTTP_HEADERS, allow_redirects=False, verify=False)
        res = r.text

    except Exception as e:
        # logger.error(e)
        update_scan_status(webapp, plugin)
        return
    if 'addEventListener' in res:
        logger.debug("[%s] [%s] %s" % (plugin, 'listening', url))
        # cmd = 'sed -i "s#www.xxx.com#%s#g" /var/www/html/wordpress/sectest/postmessage/attack.html' % url.strip('https://')
        # p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # p.communicate()
        # driver = webdriver.Chrome(executable_path='/opt/tools/chromedriver', chrome_options=chrome_options)
        # # driver.set_page_load_timeout(180)
        # try:
        #     driver.get('/sectest/postmessage/attack.html')
        #     time.sleep(5)
        #     # iframe = driver.find_elements_by_tag_name('iframe')[0]
        #     driver.switch_to.frame("otherPage")
        #     logger.debug('Can locate to iframe tag')
        #     soup = BeautifulSoup(driver.page_source, "html.parser")
        #     logger.info(soup.text)
        #     if 'dandh811' in soup.text:
        #         Risk.objects.update_or_create(target=url, risk_type="postmessage_listen", defaults={"desc": 'addEventListener'})
        #         logger.info('[$] 可能存在漏洞')
        #     else:
        #         logger.debug('未发现dandh811')
        #         update_scan_status(webapp, plugin)
        # # if '.postMessage(' in res:
        # #     logger.info("[%s] [%s] %s" % (plugin, 'sending', url))
        # #     Risk.objects.update_or_create(target=url, risk_type="postmessage_post", defaults={"desc": '.postMessage'})
        # # update_scan_status(webapp, plugin)
        # except Exception as e:
        #     logger.critical(e)
        # finally:
        #     driver.quit()
        # cmd2 = 'sed -i "s#%s#www.xxx.com#g" /var/www/html/wordpress/sectest/postmessage/attack.html' % url.strip(
        #     'https://')
        # p2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # p2.communicate()

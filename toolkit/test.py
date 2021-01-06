import requests
from lib.common import update_scan_status
import subprocess
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import socket
import time
import telnetlib

plugin = 'postmessage'

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')

url = 'https://www.yelpreservations.com'

HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
}

try:
    r = requests.get(url, timeout=10, headers=HTTP_HEADERS, allow_redirects=False, verify=False)
    res = r.text

except Exception as e:
    logger.error(e)

if 'addEventListener' in res:
    logger.debug("[%s] [%s] %s" % (plugin, 'listening', url))
    cmd = 'sed -i "s#www.xxx.com#%s#g" /var/www/html/wordpress/sectest/postmessage/attack.html' % url.strip('https://')
    logger.info(cmd)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.communicate()
    driver = webdriver.Chrome(executable_path='/opt/tools/chromedriver', chrome_options=chrome_options)
    # driver.set_page_load_timeout(10)
    try:
        driver.get('/sectest/postmessage/attack.html')
        # time.sleep(5)
        # iframe = driver.find_elements_by_tag_name('iframe')[0]
        # driver.switch_to.frame(iframe)
        driver.switch_to.frame("otherPage")

        logger.debug('Can locate to iframe tag')
        soup = BeautifulSoup(driver.page_source, "html.parser")
        if 'dandh811' in soup.text:
            logger.info('[$] 可能存在漏洞')
        else:
            logger.debug('未发现dandh811')
    # if '.postMessage(' in res:
    #     logger.info("[%s] [%s] %s" % (plugin, 'sending', url))
    #     Risk.objects.update_or_create(target=url, risk_type="postmessage_post", defaults={"desc": '.postMessage'})
    # update_scan_status(webapp, plugin)
    except Exception as e:
        logger.critical(e)
    finally:
        driver.close()
    cmd2 = 'sed -i "s#%s#www.xxx.com#g" /var/www/html/wordpress/sectest/postmessage/attack.html' % url.strip(
        'https://')
    p2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p2.communicate()

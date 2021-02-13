"""
开放重定向漏洞检测，检测场景包括：
1. 子域名直接能否跳转；
2. url中含参数能否跳转；
注册和登录场景无法实现。
"""
import requests
from apps.webapps.models import WebUrls
from apps.assets.models import Risk
from lib.common import url_is_ip
import urllib3
from lib.wechat_notice import wechat
from lib.common import update_scan_status
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib import parse
from loguru import logger
import subprocess

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

plugin = 'open_redirect'


def start(**kwargs):
    webapps = kwargs['webapps']
    policy = kwargs['policy']
    keywords = ['next', 'url', 'return', 'redirect_url', 'callback_url', 'callback', 'r', 'target', 'error', 'errurl',
                'error_url', 'redirect', 'redirect_to', 'jump', 'jump_to', 'to', 'link', 'linkto', 'domain', 'u',
                'continue', 'back_url']
    payloads = [r'\baidu.com', '/baidu.com', '//baidu.com', '///baidu.com', '////baidu.com', 'https://googel.com@baidu.com',
                '#baidu.com', '?baidu.com', r'\\baidu.com', '.baidu', '.baidu.com', '///baidu.com//..',
                '////baidu.com//..', '/http://baidu.com']
    chrome_options=Options()

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    if policy == 'full':
        weburls = WebUrls.objects.order_by('-id')
    else:
        weburls = WebUrls.objects.exclude(scanned__icontains=plugin)
        webapps = webapps.exclude(scanned__icontains=plugin)

    if not weburls:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
    for weburl in weburls:
        url = parse.unquote(weburl.url, 'utf-8')

        if url_is_ip(url):
            continue
        logger.debug("[%s] [%s] %s" % (plugin, weburl.id, url))

        try:
            browser = webdriver.Chrome(executable_path='/opt/tools/chromedriver', chrome_options=chrome_options)
        except Exception as e:
            logger.critical(e)
            continue
        risk = False

        parseResult = parse.urlparse(url)
        param_dict = parse.parse_qs(parseResult.query)

        for param in param_dict.keys():

            if param not in keywords:
                continue
            if risk:
                continue

            for payload in payloads:
                _url = url.replace(param+'='+param_dict[param][0], param+'='+payload)
                logger.debug("[%s] [%s] %s" % (plugin, weburl.id, url))
                try:
                    browser.get(url)
                    cur_url = browser.current_url
                    browser.close()
                except Exception as e:
                    continue

                if 'www.baidu' in cur_url:
                    logger.info('[$$$] success, 发现漏洞')
                    Risk.objects.update_or_create(target=url, risk_type='开放重定向', defaults={"desc": _url})

                    title = '发现开放重定向漏洞'
                    content = '-'
                    wechat.send_msg(title, content)
                    risk = True
        try:
            subprocess.call('pkill chrome', shell=True)
        except Exception as e:
            logger.critical(e)
        finally:
            browser.quit()
        update_scan_status(weburl, plugin)

    if not webapps:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
    payloads2 = [r'\baidu.com', '/baidu.com', '//baidu.com', '///baidu.com', '////baidu.com',
                '#baidu.com', '?baidu.com', r'\\baidu.com', '///baidu.com//..',
                '////baidu.com//..', '/http://baidu.com']
    for webapp in webapps:
        try:
            browser = webdriver.Chrome(executable_path='/opt/tools/chromedriver', chrome_options=chrome_options)
        except Exception as e:
            logger.critical(e)
            continue
        risk = False
        for payload in payloads2:
            if risk:
                continue
            url = webapp.subdomain + payload
            logger.debug("[%s] [%s] %s" % (plugin, webapp.id, url))
            try:
                browser.get(url)
                cur_url = browser.current_url
                browser.close()
            except Exception as e:
                cur_url = 'error'
            if 'www.baidu' in cur_url:
                logger.info('[$$$] success, 发现漏洞')
                Risk.objects.update_or_create(target=url, risk_type='开放重定向', defaults={"desc": url})

                title = '发现开放重定向漏洞'
                content = url
                wechat.send_msg(title, content)
                risk = True
        try:
            update_scan_status(webapp, plugin)
            subprocess.call('pkill chrome', shell=True)
        except Exception as e:
            logger.critical(e)
        finally:
            browser.quit()

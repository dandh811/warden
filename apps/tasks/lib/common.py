import re
import requests
import sys
import socket
import traceback
import json
# import tldextract
# from virustotal_python import Virustotal
from apps.tasks.lib.osdetect import osdetect
from urllib import parse
from apps.tasks.lib.wappalyzer import WebPage
from apps.tasks.lib.random_header import get_ua
from apps.tasks.lib.vuln import Vuln
from apps.tasks.lib.jsparse import JsParse
from apps.tasks.lib.sql_injection import sql_check
from apps.tasks.lib.iscdn import iscdn
from apps.tasks.lib.settings import TIMEOUT, virustotal_api, POC

payload = " AND 1=1 UNION ALL SELECT 1,NULL,'<script>alert(XSS)</script>',table_name FROM information_schema.tables WHERE 2>1--/**/; EXEC xp_cmdshell('cat ../../../etc/passwd')"


def update_scan_status(target, type):
    try:
        cur_scan_status = target.scanned
        if cur_scan_status == 'not':
            target.scanned = type
        elif type not in cur_scan_status:
            target.scanned = cur_scan_status + ',' + type
        target.save()
    except Exception as e:
        pass

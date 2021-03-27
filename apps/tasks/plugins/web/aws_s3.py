from apps.assets.models import Risk
from lib.wechat_notice import wechat
from lib.common import update_scan_status
import subprocess
from apps.webapps.models import Domain
import re
from urllib.parse import urlparse
from loguru import logger
from multiprocessing.dummy import Pool as ThreadPool

plugin = 'aws_s3'


def start(**kwargs):
    targets = kwargs['targets']
    webapps = kwargs['webapps']
    policy = kwargs['policy']

    if targets == '*':
        if policy == 'full':
            domains = Domain.objects.order_by('-id')
        else:
            domains = Domain.objects.exclude(scanned__icontains=plugin)
            webapps = webapps.exclude(scanned__icontains=plugin)
    else:
        targets = targets.split(',')
        if policy == 'full':
            domains = Domain.objects.filter(domain__in=targets).order_by('-id')
        else:
            domains = Domain.objects.exclude(scanned__icontains=plugin).filter(domain__in=targets)
            webapps = webapps.exclude(scanned__icontains=plugin)

    if not domains and not webapps:
        logger.debug("[%s] %s" % (plugin, '未匹配到扫描对象'))
        return

    buckets = []
    try:
        pool = ThreadPool(15)
        bucket_existent = pool.map(check_bucket_domain_is_exist, domains)
        if bucket_existent:
            buckets += bucket_existent
            logger.warning(buckets)
        pool.close()
        pool.join()
    except Exception as e:
        logger.critical(e)

    try:
        pool = ThreadPool(15)
        bucket_existent = pool.map(check_bucket_subdomain_is_exist, webapps)
        if bucket_existent:
            buckets += bucket_existent
            logger.warning(buckets)
        pool.close()
        pool.join()
    except Exception as e:
        logger.critical(e)

    if buckets:
        for bucketL in buckets:
            if bucketL:
                for bucket in bucketL:
                    # check_s3_acl(bucket)
                    if bucket:
                        check_s3_cp(bucket)


def check_bucket_domain_is_exist(domain):
    bucket_existent = []
    domain_name = domain.domain
    logger.debug("[%s] [%s] %s" % (plugin, domain.id, domain_name))

    res = check_s3_ls(domain_name)
    if res:
        bucket_existent.append(domain_name)

    domain_ = domain_name.split('.')[0]
    bucket_name_keywords = ['marketing', 'attachments', 'users', 'files']
    for keyword in bucket_name_keywords:
        bucket_name = domain_ + '.' + keyword
        res = check_s3_ls(bucket_name)
        if res:
            bucket_existent.append(bucket_name)

    update_scan_status(domain, plugin)

    return bucket_existent


def check_bucket_subdomain_is_exist(webapp):
    bucket_existent = []
    url = webapp.subdomain
    netloc = urlparse(url).netloc.split(':')[0]

    if not bool(re.search('[a-z]', netloc)):  # 判断url是域名还是IP
        return
    logger.debug("[%s] [%s] %s" % (plugin, webapp.id, url))

    sdm = url.split('//')[1]
    res = check_s3_ls(sdm)
    if res:
        bucket_existent.append(sdm)

    update_scan_status(webapp, plugin)

    return bucket_existent


def check_s3_ls(bucket):
    found = False
    try:
        command = 'aws s3 ls s3://' + bucket

        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

        res = out.decode('utf-8')
        if res and 'NoSuchBucket' not in res:
            logger.debug(res.strip())
            logger.info('Found a bucket: ' + bucket)
            found = True
            if 'Access Denied' in res or 'error' in res or 'Could not' in res or 'Connect timeout' in res:
                logger.info(res.strip())
            else:
                logger.info('[$$] bucket: %s 允许列出文件！！！' % bucket)
                Risk.objects.update_or_create(target=command, risk_type='AWS S3未授权访问', defaults={'desc': res})
    except Exception as e:
        logger.critical(e)

    return found


def check_s3_acl(bucket):
    try:
        command = 'aws s3api get-bucket-acl --bucket ' + bucket
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        res = out.decode('utf-8')

        if 'Access Denied' in res or 'error' in res or 'Could not' in res:
            logger.info(res.strip())
        else:
            logger.info('[$$] bucket: %s 允许访问ACL！！！' % bucket)
            # Risk.objects.update_or_create(target=command, risk_type='AWS S3允许访问ACL', defaults={'desc': res})
    except Exception as e:
        logger.critical(e)


def check_s3_cp(bucket):
    try:
        command = 'aws s3 cp s3_test.txt s3://' + bucket
        logger.info(command)
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        res = out.decode('utf-8')
        logger.info(res)
        if 'failed' in res or 'error' in res or 'Could not' in res:
            logger.info(res.strip())
        else:
            logger.info('[$$$] bucket: %s 允许上传文件！！！' % bucket)
            Risk.objects.update_or_create(target=command, risk_type='AWS S3未授权上传', defaults={'desc': res})
    except Exception as e:
        logger.critical(e)

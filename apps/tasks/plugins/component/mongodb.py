import pymongo
from apps.assets.models import Port, Risk
import subprocess
from lib.wechat_notice import wechat
from loguru import logger
from lib.common import update_scan_status

timeout = 2

plugin = 'mongodb'


def start(**kwargs):
    policy = kwargs['policy']
    if policy == 'full':
        ports = Port.objects.filter(service_name__icontains='mongod')
    else:
        ports = Port.objects.exclude(scanned__icontains=plugin).filter(service_name__icontains='mongod')
    if not ports:
        logger.debug("[%s] %s" % (plugin, 'There are no objects to scan'))
    for port in ports:
        ip = port.asset.ip

        logger.info('-' * 75)
        logger.debug("[%s] [%s] %s" % (plugin, port.id, ip))

        try:
            conn = pymongo.MongoClient(host=ip, port=port.port_num, serverSelectionTimeoutMS=timeout)
            database_list = conn.list_database_names()
            if not database_list:
                conn.close()
                return
            conn.close()

            cmd = "mongo %s:%s" % (ip, port.port_num)
            logger.info(cmd)
            res = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            res.stdin.write(b'show dbs; \n')
            out, err = res.communicate()
            out = out.decode('utf-8')
            desc = 'MongoDB空口令，连接上数据库后，执行了show dbs命令，获取到如下信息:\n' + str(out)
            Risk.objects.update_or_create(target=ip, risk_type='mongodb空口令', defaults={'desc': desc})

            logger.info('[$$$]success')
        except Exception as e:
            logger.error(e)
        finally:
            update_scan_status(port, plugin)

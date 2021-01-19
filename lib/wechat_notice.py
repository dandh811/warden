import json
import requests
import urllib3
from loguru import logger

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()

WEIXIN_CORPID = 'wwc880f3463df65c83'
WEIXIN_SECERT = 'vHHeFqYRtchXL_-CXhYzmCs2lR1-x25uDYApsc6Y57E'


class WeChatPub:
    s = requests.session()
    token = None

    def __init__(self):
        corpid = WEIXIN_CORPID
        secret = WEIXIN_SECERT
        self.token = self.get_token(corpid, secret)

    def get_token(self, corpid, secret):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={0}&corpsecret={1}".format(corpid, secret)
        rep = self.s.get(url, timeout=10, verify=False)
        if rep.status_code == 200:
            try:
                access_token = json.loads(rep.content.decode('utf-8'))['access_token']
                return access_token
            except Exception as e:
                logger.critical(e)
        else:
            logger.critical("request failed.")
            return None

    def send_msg(self, title, content):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + self.token
        header = {
            "Content-Type": "application/json"
        }
        form_data = {
            "touser": "@all",
            "toparty": " PartyID1 | PartyID2 ",
            "totag": " TagID1 | TagID2 ",
            "msgtype": "textcard",
            "agentid": 1000002,
            "textcard": {
                "title": title,
                "description": content,
                "url": url,
                # "btntxt": "更多"
            },
            "safe": 0
        }
        rep = self.s.post(url, data=json.dumps(form_data).encode('utf-8'), headers=header)
        if rep.status_code == 200:
            res = json.loads(rep.content.decode('utf-8'))
            logger.info(res)
            return res
        else:
            logger.critical("request failed.")
            return None


wechat = WeChatPub()


if __name__ == '__main__':
    try:
        wechat = WeChatPub()
        wechat.send_msg(title="test", content="<div class=\"gray\">2016年9月26日</div> <div class=\"normal\">test</div><div class=\"highlight\">请于2016年10月10日前联系行政同事领取</div>")
    except Exception as e:
        logger.critical(e)

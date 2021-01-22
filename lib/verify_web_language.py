import re
import requests.packages.urllib3
from loguru import logger


requests.packages.urllib3.disable_warnings()


def getinfo(r):
    result = ''

    headerinfo = ["set-cookie", "X-Powered-By"]
    try:
        for hdinfo in headerinfo:
            if hdinfo in r.headers:
                # print(hdinfo, response.headers[hdinfo])
                result = webinfo(hdinfo, r.headers[hdinfo])
            # return result
        # 判断出asp和aspx同时存在的时候，判断为asp
        # m = re.findall('href=(?:"|\'|\s)[i][/\w][/i]\.(jsp|php|aspx|asp|do|action)', response.content.decode('utf-8'), re.I)
        # if 'asp' in m and 'ASP.NET' in results:
        #     results.remove('ASP.NET')
        #     results.append('ASP')

    except Exception as e:
        logger.info(e)

    return result


def webinfo(hdinfo, vulue):
    headerinfo = ["set-cookie", "X-Powered-By"]

    for payload in payloads:
        for info in payload[hdinfo]:
            result = re.findall(info['value'], vulue)
            if len(result) > 0:
                # print(info['technology'])
                return info['technology']
        # elif result is None:
        #	return vulue


payloads = [
    {"set-cookie": [
        {
            "value": "ASPSESSIONID",
            "technology": "ASP"
        },
        {
            "value": "ASP\\.NET_SessionId",
            "technology": "ASP.NET"
        },
        {
            "value": "JSESSIONID",
            "technology": "JSP"
        },
        {
            "value": "PHPSESSID",
            "technology": "PHP"
        },
        {
            "value": "JServSessionId",
            "technology": "Apache|JS"
        },
        {
            "value": "CFID|CFTOKEN|CFMAGIC",
            "technology": "ColdFusion"
        }],
        "X-Powered-By": [
            {
                "technology": "PHP",
                # "value": "PHP[url=[\\d\\.]+]\\-\\_\\/\\ [/url]"
                "value": "PHP"

            },
            {
                "technology": "JSP",
                # "value": "JSP[url=[\\d\\.]+]\\-\\_\\/\\ [/url]"
                "value": "JSP[url=[\\d\\.]+]\\-\\_\\/\\ [/url]"

},
            {
                "technology": "ASP",
                "value": "ASP[\\/\\d\\.]*$"
            },
            {
                "technology": "ASP.NET", "value": "ASP\\.NET"
            },
            {
                "technology": "Servlet",
                "value": "Servlet[url=[\\d\\.]+]\\-\\_\\/\\ [/url]"
            },
            {
                "technology": "Tomcat",
                "value": "(JBoss|Tomcat)[\\-\\_\\/\\ ]?([\\d\\.]+)"
            }],
    }
]

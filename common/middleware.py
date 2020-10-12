import time
from django.utils.deprecation import MiddlewareMixin

MAX_REQUEST_PER_SECOND = 2  # 每秒访问次数


class RequestBlockingMiddleware(MiddlewareMixin):

    def process_request(self,request):
        now=time.time()
        request_queue = request.session.get('request_queue',[])
        if len(request_queue) < MAX_REQUEST_PER_SECOND:
            request_queue.append(now)
            request.session['request_queue']=request_queue
        else:
            time0=request_queue[0]
            if (now-time0)<1:
                time.sleep(5)

            request_queue.append(time.time())
            request.session['request_queue'] = request_queue[1:]
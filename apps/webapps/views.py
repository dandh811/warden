from django.http import HttpResponse
from django.conf import settings
from apps.webapps.models import WebApp
from django.contrib.auth.decorators import login_required


@login_required
def webapp_report(request, webapp_id):
    """ 扫描报告 """
    if request.method == "GET":
        webapp = WebApp.objects.get(id=webapp_id)
        filepath = settings.BASE_DIR + webapp.report
        with open(filepath, 'rb') as html:
            response = HttpResponse(html, content_type='text/html')
            response['Content-Disposition'] = 'inline;filename=%s' % webapp.report
            return response

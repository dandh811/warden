from apps.tasks import models
from apps.tasks.asset_discovery import asset_discovery
from apps.tasks.subdomain_scan import subdomain_scan
from apps.tasks.vul_scan import vul_scan
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


@login_required
@csrf_exempt
def task_action(request, id):
    if request.method == 'GET':
        task = models.Task.objects.get(id=id)
        type = task.type
        eval(type)(task)

        return HttpResponseRedirect('/admin/tasks/task/')

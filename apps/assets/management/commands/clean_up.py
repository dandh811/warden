from apps.assets.models import Asset, Port
from apps.webapps.models import WebApp
from django.db.models import Q, Count
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "清理系统中无效或者重复资产"

    def handle(self, *args, **options):
        print(help)
        clean()

        print('+ Job done')


def clean():
    assets = Asset.objects.all()
    webapps = WebApp.objects.all()

    for asset in assets:
        ip = asset.ip

        if webapps.filter(ip=ip).exists():
            pass
        else:
            print('[-] abandoned asset %s' % ip)
            asset.delete()

    for webapp in webapps:
        scanned = webapp.scanned
        if ',postmessage' in scanned:
            scanned = scanned.replace(',postmessage', '')
            webapp.scanned = scanned
            webapp.save()


    # dupes = WebApp.objects.values('subdomain').annotate(num_subdomain=Count(':q'
    #                                                                         ''
    #                                                                         ':q'
    #                                                                         '    ')).order_by().filter(
    #     num_subdomain__gt=1)
    # # print(dupes)
    # if dupes:
    #     webapps = WebApp.objects.filter(subdomain__in=[item['subdomain'] for item in dupes])
    #     # for webapp in webapps:
    #     # print(webapp.subdomain)
    #     webapps[0].delete()

"""
财务统计信息
"""
from django.core.management.base import BaseCommand
from apps.financial.models import *
import time, datetime
from loguru import logger
from django.db.models import Max,Avg,F,Q, Sum
from lib.wechat_notice import wechat


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.debug('【家庭理财简报】')
        investments = Investment.objects.all()
        c_time = time.strftime("[简报时间] %Y年%m月%d日\n", time.localtime())
        logger.info(c_time)
        capital = Investment.objects.filter(completed='no').aggregate(nums=Sum("capital"))
        total_principal = '[总投本金] %s\n' % capital['nums']
        get_interest = 0
        interest_day = 0
        for i in investments:
            if i.completed == 'yes':
                # 如果该笔投资已经完成，所有总收益直接加入该笔投资的总收益，否则按投资天数计算；
                # 如果该笔投资已经完成，每日收益忽略；
                get_interest += i.interest_total
            else:
                get_interest += i.interest_day * (datetime.date.today() - i.start_date).days
                interest_day += i.interest_day
        get_interest = '[已得利息] %s\n' % get_interest
        interest_day = '[今日利息] %s\n' % interest_day

        latest_inv = Investment.objects.filter(completed='no').earliest('end_date')
        latest_inv_info = '[即将回款] %s:%s:%d:%s:%s\n' % (latest_inv.platform, latest_inv.bank, latest_inv.capital, latest_inv.end_date, latest_inv.investors)

        title = '【家庭理财简报】'
        content = c_time + total_principal + get_interest + interest_day + latest_inv_info
        wechat.send_msg(title, content)

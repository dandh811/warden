from django import template

register = template.Library()


@register.filter
def risk_status_display(status):
    status_dict = {
        "unconfirm": "未确认",
        "ignore": "忽略",
        "unfix": "未修复",
        "fixed": "已修复"
    }

    status_display = ''

    if status in status_dict.keys():
        status_display = status_dict.get(status)

    return status_display
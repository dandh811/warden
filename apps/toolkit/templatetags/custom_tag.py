from django import template
import time

register = template.Library()  # 注册过滤器


@register.filter
def int_to_list(number):
    new_list = range(0, number)

    return new_list

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import django.utils.timezone as timezone
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from apps.tasks.models import Task

yes_or_no = (
    ('yes', '是'),
    ('no', '否')
)


class Platform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, default='', verbose_name="购买平台")
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '购买平台'
        verbose_name_plural = verbose_name


class Bank(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, default='', verbose_name="银行")
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '银行'
        verbose_name_plural = verbose_name


class Investors(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, default='', verbose_name="投资人")
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '投资人'
        verbose_name_plural = verbose_name


class Investment(models.Model):
    id = models.AutoField(primary_key=True)
    platform = models.ForeignKey(Platform, verbose_name="购买平台", on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, verbose_name="银行名称", on_delete=models.CASCADE, default='')
    investors = models.ForeignKey(Investors, verbose_name="投资人", on_delete=models.CASCADE)
    year_rate = models.DecimalField(default=0, max_digits=4, decimal_places=3, verbose_name="年化利率", )
    start_date = models.DateField(verbose_name="开始日期")
    end_date = models.DateField(verbose_name="结束日期")
    loan_days = models.DecimalField(default=0, max_digits=4, decimal_places=0, verbose_name="投资期限(天)")
    capital = models.DecimalField(default=0, max_digits=10, decimal_places=0, verbose_name="投资本金(元)")
    m_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    desc = models.CharField(max_length=200, default='', verbose_name="备注", null=True, blank=True)
    completed = models.CharField(choices=yes_or_no, default='no', max_length=5, verbose_name='是否已完成')
    interest_total = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="总收益")
    interest_day = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="每天收益")

    def __str__(self):
        return '%s' % self.id

    class Meta:
        verbose_name = '投资列表'
        verbose_name_plural = verbose_name

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError({'end_date': '投资结束日期应该晚于开始日期'})

    def save(self, *args, **kwargs):
        self.loan_days = (self.end_date - self.start_date).days
        self.interest_day = round(self.year_rate * (self.capital/100) / 365, 2)
        self.interest_total = self.interest_day * self.loan_days
        super().save(*args, **kwargs)

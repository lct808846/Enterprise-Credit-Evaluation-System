from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime

class Astock(models.Model):
    stockid = models.CharField(max_length=64)
    stockname = models.CharField(max_length=64)
    company = models.CharField(max_length=64)
    createtime = models.CharField(max_length=64)  # 考虑使用DateTimeField或DateField以更好地处理日期时间数据
    category = models.CharField(max_length=64)
    desc = models.TextField(blank=True, null=True)  # blank 和 null 参数允许该字段为空


    class Meta:
        db_table = 'astock'  # 指定数据库表名


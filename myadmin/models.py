from django.db import models

# Create your models here.
from django.db import models
from datetime import datetime

#用户账号信息模型
class User(models.Model):
    username = models.CharField(max_length=50)    #员工账号
    nickname = models.CharField(max_length=50)    #昵称
    password_hash = models.CharField(max_length=100)#密码
    password_salt = models.CharField(max_length=50)    #密码干扰值
    status = models.IntegerField(default=1)    #状态:1正常/2禁用/9删除
    create_at = models.DateTimeField(default=datetime.now)    #创建时间
    update_at = models.DateTimeField(default=datetime.now)    #修改时间

    def toDict(self):
        return {'id':self.id,'username':self.username,'nickname':self.nickname,'password_hash':self.password_hash,'password_salt':self.password_salt,'status':self.status,'create_at':self.create_at.strftime('%Y-%m-%d %H:%M:%S'),'update_at':self.update_at.strftime('%Y-%m-%d %H:%M:%S')}

    class Meta:
        db_table = "user"  # 更改表名


class Astock(models.Model):
    stockid = models.CharField(max_length=64)
    stockname = models.CharField(max_length=64)
    company = models.CharField(max_length=64)
    createtime = models.CharField(max_length=64)  # 考虑使用DateTimeField或DateField以更好地处理日期时间数据
    category = models.CharField(max_length=64)
    desc = models.TextField(blank=True, null=True)  # blank 和 null 参数允许该字段为空


    class Meta:
        db_table = 'astock'  # 指定数据库表名


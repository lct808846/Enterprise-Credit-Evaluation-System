from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class EnterpriseAll(models.Model):
    # 定义字段，并指定数据类型和选项
    firm_eid = models.TextField(null=True, blank=True)
    firm_name = models.TextField(null=True, blank=True)
    legal_rep = models.TextField(null=True, blank=True)
    est_date = models.DateField(null=True, blank=True)
    open_date = models.DateField(null=True, blank=True)
    bd_longitude = models.FloatField(null=True, blank=True)
    bd_latitude = models.FloatField(null=True, blank=True)
    reg_cap = models.FloatField(null=True, blank=True)
    ope_scope = models.TextField(null=True, blank=True)
    execute_one_year = models.TextField(null=True, blank=True)
    execute_two_year = models.TextField(null=True, blank=True)
    execute_three_year = models.TextField(null=True, blank=True)
    case_one_year = models.TextField(null=True, blank=True)
    case_two_year = models.TextField(null=True, blank=True)
    case_three_year = models.TextField(null=True, blank=True)
    one_all_money = models.TextField(null=True, blank=True)
    two_all_money = models.TextField(null=True, blank=True)
    three_all_money = models.TextField(null=True, blank=True)
    judge_one_year = models.TextField(null=True, blank=True)
    judge_two_year = models.TextField(null=True, blank=True)
    judge_three_year = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'enterprise_all'  # 指定数据库中的表名

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# 自动创建或更新Profile当User被创建或更新时
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
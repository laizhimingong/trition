from django.db import models

# Create your models here.
class UserInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50, verbose_name='用户名')
    password = models.CharField(max_length=50, verbose_name='密码')
    email = models.CharField(max_length=50, verbose_name='邮箱',blank=True)
    # phone = models.CharField(max_length=20, verbose_name='手机号码',blank=True)
    def __str__(self):
        return self.username
    class Meta:
        db_table = 'UserInfo'
        ordering = ['id']
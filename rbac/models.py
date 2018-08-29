from django.db import models


class UserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name='用户名',max_length=32)
    password = models.CharField(verbose_name='密码',max_length=64)
    email = models.CharField(verbose_name='邮箱',max_length=32)
    roles = models.ManyToManyField(verbose_name='用户角色',to="Role",blank=True)

    def __str__(self):
        return self.username


class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(verbose_name='角色权限',to='Permission',blank=True)

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='标题',max_length=32)
    url = models.CharField(max_length=64)


    def __str__(self):
        return self.title





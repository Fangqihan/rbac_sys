from django.contrib import admin
from rbac import models


class Permission_admin(admin.ModelAdmin):
    list_display = ['title','url']


admin.site.register(models.UserInfo)
admin.site.register(models.Role)
admin.site.register(models.Permission,Permission_admin)
admin.site.register(models.PermissonGroup)





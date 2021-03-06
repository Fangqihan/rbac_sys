from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,redirect
import re

from rbac.views import PermissionsActions, PermissionGroup


class Md1(MiddlewareMixin):
    def process_request(self, request):

        # 1、设置白名单，过滤请求登录、注册和admin后台页面
        valid_url_list = ['/rbac/login/','/admin/','/rbac/register/', '/rbac/index/', '/rbac/logout/']
        for p in valid_url_list:
            if re.match(p, request.path) : return None

        # 2、超级用户免所有权限
        if request.user.is_superuser:
            return None

        # 3、过滤未登录用户
        if not request.session.get('user_id',''):
            return redirect('/rbac/login/')

        # 4、获取当前用户的所有权限
        permissions_dict = request.session.get('permissions_dict')
        print('permissions_dict==========',permissions_dict)

        # 5、判断当前用户是否有权限访问此路径
        flags = False
        # {1:{urls:[],actions:[]}, 2:{urls:[],actions:[]}}
        for item in permissions_dict.values():
            for p in item['urls']:
                if re.fullmatch(p,request.path):
                    flags=True
                    request.actions = PermissionsActions(item['actions'])
                    break

        if not flags:
            return render(request, 'rbac/page_403.html')

    def process_response(self, request, response):
        # print('md1_process_response')
        return response  # 必须带返回值

## 思路
model表设计：
![](http://oyhijg3iv.bkt.clouddn.com/rbac%E6%9D%83%E9%99%90%E5%88%86%E9%85%8D%E6%80%9D%E8%B7%AF.png)


## 权限认证

#### 登录认证
在登录时取出当前用户的权限信息，并且将其转换为特定格式：

```python
# 其中1、2为权限组id，内部字典中包含拥有对应组的所有的权限urls和对应的操作（增/删/改/查）
permission_dict = {
    1: {'urls': ['/rbac/users/', '/rbac/users/', '/rbac/users/add/', '/rbac/users/edit/(\\d+)/', '/rbac/users/delete/(\\d+)/'],
        'actions': ['list', 'add', 'edit', 'delete']},
    2: {'urls': ['/rbac/roles/', '/rbac/roles/delete/(\\d+)/', '/rbac/roles/add/', '/rbac/roles/edit/(\\d+)/'],
        'actions': ['list', 'delete', 'add', 'edit']}
     }
```


```python
def my_login(request):
    """登录逻辑"""
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserInfo.objects.filter(username=username,password=password).first()
        if user:
            # 1、在当前session保存用户信息
            request.session['user_id']= user.id
            request.session['username']= user.username

            # 2、取出当前用户的相关权限信息并转化成需要的格式
            query = list(user.roles.values('permissions__url','permissions__action',
                                           'permissions__permission_group').distinct())
            rest = {}
            for item in query:
                gid = item['permissions__permission_group']
                if not rest.keys():
                    rest[gid] = {}
                    rest[gid]['urls'] = [item['permissions__url'], ]
                    rest[gid]['actions'] = [item['permissions__action']]

                if gid in rest.keys():
                    if item['permissions__url'] not in rest[gid]['urls']:
                        rest[gid]['urls'].append(item['permissions__url'])
                    if item['permissions__action'] not in rest[gid]['actions']:
                        rest[gid]['actions'].append(item['permissions__action'])

                if gid not in rest.keys():
                    rest[gid] = {}
                    rest[gid]['urls'] = [item['permissions__url'], ]
                    rest[gid]['actions'] = [item['permissions__action']]
            # 保存到session中
            request.session['permissions_dict'] = rest

            # 3、取出当前用户的相关菜单-权限内容并转化后才能需要的格式，最后保存
            query_menu = list(user.roles.values('permissions__menu','permissions__url', 'permissions__title').distinct())
            print('query_menu==========', query_menu)
            res = []
            for item in query_menu:
                if item['permissions__menu']:
                    t = (item['permissions__url'], item['permissions__title'])
                    res.append(t)
            request.session['permissions_menu_list'] = res

            return redirect('/rbac/index/')

    return render(request, 'rbac/login.html')
```

菜单转换后的格式：

```
l = [
    {'permissions__menu': True, 'permissions__url': '/rbac/users/', 'permissions__title': '查询用户'},
    {'permissions__menu': False, 'permissions__url': '/rbac/users/add/', 'permissions__title': '添加用户'},
    {'permissions__menu': True, 'permissions__url': '/rbac/roles/', 'permissions__title': '查看角色'},
    {'permissions__menu': False, 'permissions__url': '/rbac/users/edit/(\\d+)/', 'permissions__title': '编辑用户'}]
```


#### 自定义中间件过滤请求

```
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
```


#### 前端逻辑判断

```python
# views.py
class PermissionsActions:
    """供前端调用使用，判断当前操作是否有权限"""
    def __init__(self, actions):
        self.actions = actions

    def add(self):
        return 'add' in self.actions

    def delete(self):
        return 'delete' in self.actions

    def edit(self):
        return 'edit' in self.actions

    def list(self):
        return 'list' in self.actions
```


```python
# middleware.py
class Md1(MiddlewareMixin):
    def process_request(self, request):
        ...
        # 5、判断当前用户是否有权限访问此路径
        flags = False
        # {1:{urls:[],actions:[]}, 2:{urls:[],actions:[]}}
        for item in permissions_dict.values():
            for p in item['urls']:
                # 用户的请求路径匹配
                if re.fullmatch(p,request.path):
                    flags=True
                    # 将当前权限组的actions放进request中，例如当前请求路径为角色组，那么就会将角色相关的action放到request中
                    request.actions = PermissionsActions(item['actions'])
                    break

        if not flags:
            return render(request, 'rbac/page_403.html')

    def process_response(self, request, response):
        pass
```

```
{% if request.actions.add %}
    <a href="{% url 'role_add' %}" ><button class="btn btn-info">新增角色</button></a>
{% endif %}
```


#### 界面展示
![](http://oyhijg3iv.bkt.clouddn.com/rbac%E7%95%8C%E9%9D%A2.png)



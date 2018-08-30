from django.shortcuts import render, HttpResponse, redirect
from .models import UserInfo, Role


def get_users(request):
    user_list = UserInfo.objects.all()
    return render(request, 'rbac/user_list.html', locals())


def get_roles(request):
    role_list = Role.objects.all()
    return render(request, 'rbac/role_list.html', locals())


def add_user(request):

    if request.method == "POST":
        # 3、用户发起post请求
        form = UserInfoForm(data=request.POST)
        # 4、检测输入的值是否符合form的字段要求
        if form.is_valid():
            # 5、没有错误才能进行数据保存
            form.save()
            return redirect('/rbac/users/')

    form = UserInfoForm()
    return render(request, 'rbac/add_user.html',locals())


def delete_user(request,id):
    user = UserInfo.objects.filter(id=id).first()
    if not user:
        return render(request, 'rbac/page_404.html')

    user.delete()
    return redirect('/rbac/users/')



from .forms import UserInfoForm,RoleForm

def edit_user(request,id):
    user = UserInfo.objects.filter(id=id).first()
    if not user:
        return render(request, 'rbac/page_404.html')

    if request.method == "POST":
        # 3、用户发起post请求
        form = UserInfoForm(instance=user, data=request.POST)
        # 4、检测输入的值是否符合form的字段要求
        if form.is_valid():
            # 5、没有错误才能进行数据保存
            form.save()
            return redirect('/rbac/users/')

    form = UserInfoForm(instance=user)
    return render(request, 'rbac/edit_user.html', locals())


def add_role(request):
    if request.method == 'POST':
        form = RoleForm(data=request.POST)
        # 4、检测输入的值是否符合form的字段要求
        if form.is_valid():
            # 5、没有错误才能进行数据保存
            form.save()
            return redirect('/rbac/roles/')
    form = RoleForm()
    return render(request, 'rbac/add_role.html', locals())


def edit_role(request, id):
    role = Role.objects.filter(id=int(id)).first()
    if not role:
        return render(request, 'rbac/page_404.html')

    if request.method == 'POST':
        form = RoleForm(instance=role, data=request.POST)
        # 4、检测输入的值是否符合form的字段要求
        if form.is_valid():
            # 5、没有错误才能进行数据保存
            form.save()
            return redirect('/rbac/roles/')

    form = RoleForm(instance=role)
    return render(request, 'rbac/edit_role.html', locals())



def delete_role(request, id):
    role = Role.objects.filter(id=id).first()
    if not role:
        return render(request, 'rbac/page_404.html')

    role.delete()
    return redirect('/rbac/roles/')


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


class PermissionGroup:
    def __init__(self, key_list):
        self.key_list = key_list

    def role_manage(self):
        return 2 in self.key_list

    def user_manage(self):
        return 1 in self.key_list


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
            request.session['permissions_dict'] = rest  # 包含权限名称的权限类别

            query_menu = list(user.roles.values('permissions__menu','permissions__url', 'permissions__title').distinct())
            print('query_menu==========', query_menu)
            res = []

            for item in query_menu:
                if item['permissions__menu']:
                    t = (item['permissions__url'], item['permissions__title'])
                    res.append(t)
            # print('res',res)

            request.session['permissions_menu_list'] = res
            return redirect('/rbac/index/')

    return render(request, 'rbac/login.html')


def homepage(request):
    pass
    return render(request, 'rbac/index.html')


def my_logout(request):
    request.session.delete()
    return redirect('/rbac/login/')


def my_register(request):
    pass

    return





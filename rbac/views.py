from django.shortcuts import render, HttpResponse, redirect
from .models import UserInfo, Role


def get_users(request):
    user_list = UserInfo.objects.all()
    return render(request, 'rbac/user_list.html', locals())


def get_roles(request):
    role_list = Role.objects.all()
    return render(request, 'rbac/role_list.html', locals())


def add_user(request):
    return HttpResponse('<h1>新增用户</h1>')


def delete_user(request,id):
    user = UserInfo.objects.filter(id=id).first()
    if not user:
        return render(request, 'rbac/page_404.html')

    user.delete()
    return redirect('/rbac/users/')



from .forms import UserInfoForm

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
    return render(request, 'rbac/edit_info.html', locals())



def my_login(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = UserInfo.objects.filter(username=username,password=password).first()
        if user:
            # 1、在当前session保存用户信息
            request.session['user_id']= user.id
            request.session['username']= user.username

            # 2、获取当前用户的所有权限
            permission_list = []
            res = list(user.roles.values('permissions__url','permissions__title').distinct())
            print(res)
            for p in res:
                permission_list.append(p['permissions__url'])

            # 3、在当前session中当前用户的所有权限信息
            request.session['permission_list'] = permission_list  # 权限url列表
            request.session['permissions_query'] = res  # 包含权限名称的权限类别
            return redirect('/rbac/index/')

    return render(request, 'rbac/login.html')



def homepage(request):
    return render(request, 'rbac/index.html')


def my_logout(request):
    request.session.delete()
    return redirect('/rbac/login/')


def my_register(request):
    pass

    return

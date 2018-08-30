"""rbac_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from rbac import views as rbac_view

urlpatterns = [
    url(r'users/$', rbac_view.get_users, name='user_list'),
    url(r'index/$', rbac_view.homepage),
    url(r'users/add/$', rbac_view.add_user, name='user_add'),
    url(r'users/edit/(\d+)/$', rbac_view.edit_user, name='user_edit'),
    url(r'users/delete/(\d+)/$', rbac_view.delete_user, name='user_delete'),

    url(r'roles/$', rbac_view.get_roles, name='role_list'),
    url(r'roles/add/$', rbac_view.add_role, name='role_add'),
    url(r'roles/edit/(\d+)/$', rbac_view.edit_role, name='role_edit'),
    url(r'roles/delete/(\d+)/$', rbac_view.delete_role, name='role_delete'),

    url(r'login/$', rbac_view.my_login, name='rbac_login'),
    url(r'logout/$', rbac_view.my_logout, name='rbac_logout'),
    url(r'register/$', rbac_view.my_register, name='rbac_register'),

]




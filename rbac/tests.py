from django.test import TestCase

# Create your tests here.


# l = [{'permissions__url': '/rbac/users/', 'permissions__action': 'list', 'permissions__permission_group': 1},
#      {'permissions__url': '/rbac/users/add/', 'permissions__action': 'add', 'permissions__permission_group': 1},
#      {'permissions__url': '/rbac/roles/', 'permissions__action': 'list', 'permissions__permission_group': 2},
#      {'permissions__url': '/rbac/users/edit/(\\d+)/', 'permissions__action': 'edit', 'permissions__permission_group': 1},
#      {'permissions__url': '/rbac/users/delete/(\\d+)/', 'permissions__action': 'delete', 'permissions__permission_group': 1},
#      {'permissions__url': '/rbac/roles/delete/(\\d+)/', 'permissions__action': 'delete', 'permissions__permission_group': 2},
#      {'permissions__url': '/rbac/roles/add/', 'permissions__action': 'add', 'permissions__permission_group': 2},
#      {'permissions__url': '/rbac/roles/edit/(\\d+)/', 'permissions__action': 'edit', 'permissions__permission_group': 2}]
#
# rest = {}
#
# for item in l:
#     gid = item['permissions__permission_group']
#     if not rest.keys():
#         rest[gid]={}
#         rest[gid]['urls']=[item['permissions__url'],]
#         rest[gid]['actions']=[item['permissions__action']]
#
#     if gid in rest.keys():
#         rest[gid]['urls'].append(item['permissions__url'])
#         if item['permissions__action'] not in rest[gid]['actions']:
#             rest[gid]['actions'].append(item['permissions__action'])
#
#     if gid not in rest.keys():
#         rest[gid] = {}
#         rest[gid]['urls'] = [item['permissions__url'], ]
#         rest[gid]['actions'] = [item['permissions__action']]
#
#
# print(rest)


d = {1: {'urls': ['/rbac/users/', '/rbac/users/', '/rbac/users/add/', '/rbac/users/edit/(\\d+)/', '/rbac/users/delete/(\\d+)/'],
         'actions': ['list', 'add', 'edit', 'delete']},
     2: {'urls': ['/rbac/roles/', '/rbac/roles/delete/(\\d+)/', '/rbac/roles/add/', '/rbac/roles/edit/(\\d+)/'],
         'actions': ['list', 'delete', 'add', 'edit']}
     }
#
#
# print(d.values())
#
# l = [{'permissions__menu': True, 'permissions__url': '/rbac/users/', 'permissions__title': '查询用户'}, {'permissions__menu': False, 'permissions__url': '/rbac/users/add/', 'permissions__title': '添加用户'}, {'permissions__menu': True, 'permissions__url': '/rbac/roles/', 'permissions__title': '查看角色'}, {'permissions__menu': False, 'permissions__url': '/rbac/users/edit/(\\d+)/', 'permissions__title': '编辑用户'}]
#
# res = []
#
# for item in l:
#     if item['permissions__menu']:
#         t = (item['permissions__url'], item['permissions__title'])
#         res.append(t)
#
# print(res)


l = [
    {'permissions__menu': True, 'permissions__url': '/rbac/users/', 'permissions__title': '查询用户'},
    {'permissions__menu': False, 'permissions__url': '/rbac/users/add/', 'permissions__title': '添加用户'},
    {'permissions__menu': True, 'permissions__url': '/rbac/roles/', 'permissions__title': '查看角色'},
    {'permissions__menu': False, 'permissions__url': '/rbac/users/edit/(\\d+)/', 'permissions__title': '编辑用户'}]


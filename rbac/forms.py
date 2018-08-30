from django.forms import ModelForm, Textarea,CharField
from rbac.models import UserInfo, Role


class UserInfoForm(ModelForm):

    class Meta:
        model = UserInfo
        # 显示所有字段
        fields = '__all__'
        # 排除显示的字段
        # exclude = ['gender']

        # 修改label的text值，即字段显示名称
        # labels = {
        #     'name': ('Writer'),
        # }

        # 修改对应字段的标签类型和显示样式
        widgets = {
            'name': Textarea(attrs={'cols': 40, 'rows': 10}),
        }
        error_messages = {
            'name': {
                'max_length': ("This writer's name is too long."),
                'required': ("字段不能为空"),
            },
        }

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class':'form-control'})


class RoleForm(ModelForm):

    class Meta:
        model = Role
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)

        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attrs.update({'class':'form-control'})



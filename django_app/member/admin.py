from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import MyUser


class MyUserAdmin(UserAdmin):
    # 필요한 요소만 상속구현
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('nickname', 'gender', 'email')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2','email'),
        }),
    )

    list_display = ('username', 'nickname')
    list_filter = ('is_staff', 'is_superuser')


admin.site.register(MyUser, MyUserAdmin)

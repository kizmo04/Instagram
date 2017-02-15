from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        # create_user는 is staff처리를 안해줘서 관리자 로그인 못 함
        # is staff의 디폴트 False했기 때문에 여기서 설정해준다
        # return self.create_user(username, password)
        user = self.model(
            username=username
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    CHOICES_GENDER = (
        ('m', 'Male'),
        ('f', 'Female')
    )
    # 기본값
    # password
    # last_login
    # is_active

    username = models.CharField(max_length=30, unique=True)
    nickname = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    def get_full_name(self):
        return '{} ({})'.format(
            self.nickname,
            self.username
        )

    def get_short_name(self):
        return self.nickname

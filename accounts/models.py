from typing import Optional
import hashlib

from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, user_id: str, password: Optional[str] = None, **extra_fields) -> 'User':
        if not user_id:
            raise ValueError('user_id は必須です')
        user = self.model(user_id=user_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id: str, password: Optional[str] = None, **extra_fields) -> 'User':
        return self.create_user(user_id, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    comment = models.CharField(max_length=100, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = []

    # 管理画面での表示のインスタンスメソッド
    def __str__(self):
        return self.user_id


def in_30_days():
    return timezone.now() + timedelta(days=30)


class AccessToken(models.Model):
    # トークンと紐づくユーザー
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ハッシュ化した文字列をトークンとして使用するため
    token = models.CharField(max_length=64)
    access_datetime = models.DateTimeField(default=in_30_days)

    @staticmethod
    def create_token(user: User) -> str:
        # トークンがすでに存在している場合は削除
        AccessToken.objects.filter(user=user).delete()

        # トークン作成(user_id + password +システム日付のハッシュ値とする)
        dt = timezone.now()
        str = user.user_id + user.password + dt.strftime('"%Y/%m/%d %H:%M:%S"')
        hash = hashlib.sha256(str.encode('utf-8')).hexdigest()

        # トークンをDBに追加
        token = AccessToken.objects.create(
            user=user,
            token=hash
        )
        return token

    # 管理画面での表示のインスタンスメソッド
    def __str__(self):
        dt = timezone.localtime(self.access_datetime).strftime("%Y/%m/%d %H:%M:%S")
        return f"{self.user.user_id} {(dt)} - {self.token}"

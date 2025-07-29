# your_app/authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone
from .models import AccessToken

class BearerAccessTokenAuthentication(BaseAuthentication):
    """
    Authorization: Bearer <token> を認識するカスタム認証クラス
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        # フォーマット: "Bearer xxxxxxx"
        try:
            prefix, token = auth_header.split()
        except ValueError:
            raise AuthenticationFailed("不正な認証ヘッダー形式です")

        if prefix.lower() != "bearer":
            return None  # 他の方式は無視

        try:
            token_obj = AccessToken.objects.get(token=token)
        except AccessToken.DoesNotExist:
            raise AuthenticationFailed("無効なトークンです")

        if token_obj.access_datetime < timezone.now():
            raise AuthenticationFailed("トークンの有効期限が切れています")

        # 認証成功: (user, auth) を返す
        return (token_obj.user, None)

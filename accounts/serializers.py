from .models import User
from typing import Any

from rest_framework import serializers
from django.contrib.auth.hashers import check_password


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('user_id', 'password', 'confirm_password')
        # 新規登録時にpasswordを表示しない設定
        extra_kwargs = {'password': {'write_only': True}}

    # user_idのバリデーション
    def validate_user_id(self, value: str) -> str:
        # UserIDがすでに使われていた場合
        if User.objects.filter(user_id=value).exists():
            raise serializers.ValidationError("そのuser_idは既に使われています。")
        return value

    # attrsは全てを含んだ辞書の意味合い
    # 今回はパスワードはテキトーなのでバリデーションは行わない
    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        # パスワードと確認用パスワードが一致してることを確認
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("パスワードが一致しません。")
        return attrs

    def create(self, validated_data: dict[str, Any]) -> User:
        # DBに保存しないため削除
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=20)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        # リクエストデータのうちuser_idとpasswordを取得
        request_user_id = attrs.get('user_id')
        request_password = attrs.get('password')
        try:
            user = User.objects.get(user_id=request_user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("ユーザーIDが存在しません")
        if not check_password(request_password, user.password):
            raise serializers.ValidationError("パスワードが正しくありません")

        attrs['user'] = user
        return attrs


class DeleteProfileSerializer(serializers.Serializer):
    def validate(self, attrs: dict[str, Any]) -> None:
        request_user_id = attrs.get('user_id')
        request_password = attrs.get('password')

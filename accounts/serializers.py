from rest_framework import serializers
from .models import User
from typing import Any

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'password')
        # 新規登録時にpasswordを表示しない設定
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data: dict[str, Any]) -> User:
        user = User.objects.create_user(**validated_data)
        return user

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

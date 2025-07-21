import traceback

from .serializers import RegisterSerializer, LoginSerializer
from typing import Any
from .models import User, AccessToken

from django.db import IntegrityError, DataError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    """
    新規ユーザー登録用のAPIビュー

    POST:
        ユーザー情報を受け取り、新しいユーザーを作成します
        必須フィールド： user_id, password, confirm_password
    """
    permission_classes = [AllowAny]

    def post(self, request: dict[str, Any]) -> Response:
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        # serializerによるバリデーションチェック
        if serializer.is_valid(raise_exception=True):
            # エラーなし
            try:
                serializer.save()
                return Response(serializer.data, status=HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {'error': '一意制約違反'},
                    status=HTTP_500_INTERNAL_SERVER_ERROR
                )
            except DataError:
                return  Response(
                    {'error': 'データ形式エラー'},
                    status=HTTP_400_BAD_REQUEST
                )
            except Exception:
                return Response(
                    {'error': '予期せぬエラー'},
                    status=HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    ユーザーログイン用のAPIビュー

    POST:
        ユーザー情報を受け取り、ユーザー情報を照合し、ログイン処理を行います
        必須フィールド： user_id, password
    """
    permission_classes = [AllowAny]

    def post(self, request: dict[str, Any]) -> Response:
        print(request.data)
        serializer = LoginSerializer(data=request.data)
        # serializerによるバリデーションチェック
        if serializer.is_valid(raise_exception=True):
            try:
                # アクセストークンの生成
                AccessToken.create_token(serializer.validated_data['user'])
                return Response(
                    {'detail': 'ログインに成功しました'},
                    status=HTTP_200_OK
                )
            except DataError:
                return  Response(
                    {'error': 'データ形式エラー'},
                    status=HTTP_400_BAD_REQUEST
                )
            except Exception as e:
                print(str(e))
                traceback.print_exc()
                return Response(
                    {'error': '予期せぬエラー'},
                    status=HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
            {'error': 'ログインに失敗しました'},
            status=HTTP_400_BAD_REQUEST
        )

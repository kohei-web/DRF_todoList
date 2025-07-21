from .serializers import RegisterSerializer
from typing import Any
from .models import  User

from django.db import IntegrityError, DataError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    def post(self, request: dict[str, Any]):
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

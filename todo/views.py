from .models import TodoList
from .serializers import AddTodoListSerializer

from django.db import IntegrityError, DataError

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR


class TodoCreateView(APIView):
    """
    新規Todo登録用のAPIビュー

    POST:
        Todo情報を受け取り、新しいTodoListを作成します
        必須フィールド： title, text
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializers = AddTodoListSerializer(data=request.data)
        if serializers.is_valid():
            try:
                serializers.save(user=request.user)
                return Response(
                    serializers.data, status=HTTP_201_CREATED
                )
            except IntegrityError:
                return Response(
                    {'error': '一意制約違反'},
                    status=HTTP_500_INTERNAL_SERVER_ERROR
                )
            except DataError:
                return Response(
                    {'error': 'データ形式エラー'},
                    status=HTTP_400_BAD_REQUEST
                )
            except Exception:
                return Response(
                    {'error': '予期せぬエラー'},
                    status=HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(serializers.errors, status=HTTP_400_BAD_REQUEST)


# class TodoUpdateView(APIView):

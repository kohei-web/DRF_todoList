from .models import TodoList
from .serializers import AddTodoListSerializer, UpdateTodoListSerializer, GetTodoListSerializer

from django.db import IntegrityError, DataError

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR


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


class TodoUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            todo = TodoList.objects.get(pk=pk, user=request.user)
        except TodoList.DoesNotExist:
            return Response(
                {'error': '指定されたTodoが存在しません'},
                status=HTTP_404_NOT_FOUND
            )

        serializer = UpdateTodoListSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class TodoGetView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, pk):
        try:
            todo = TodoList.objects.get(pk=pk)
        except TodoList.DoesNotExist:
            return Response(
                {'error': 'todoを取得できません'},
                status=HTTP_404_NOT_FOUND
            )
        serializer = GetTodoListSerializer(todo)
        return Response(serializer.data, status=HTTP_200_OK)


class TodoDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            todo = TodoList.objects.get(pk=pk, user=request.user)
        except TodoList.DoesNotExist:
            return Response(
                {'error': '対象のtodoが存在しません'},
                status=HTTP_404_NOT_FOUND
            )

        todo.delete()
        return Response(status=HTTP_204_NO_CONTENT)

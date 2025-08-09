from . import views
from django.urls import path, include


urlpatterns = [
    # todo追加
    path('create/', views.TodoCreateView.as_view(), name='create-todo'),
    # todo更新
    path('update/<int:pk>', views.TodoCreateView.as_view(), name='update-todo'),
    # todo取得
    path('get/<int:pk>', views.TodoGetView.as_view(), name='get-todo'),
    # todo一覧取得
    path('get/', views.TodoListGetView.as_view(), name='get-todo-list'),
    # todo削除
    path('delete/<int:pk>', views.TodoDeleteView.as_view(), name='delete-todo'),
]

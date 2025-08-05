from . import views
from django.urls import path, include


urlpatterns = [
    # todo追加
    path('create/', views.TodoCreateView.as_view(), name='create-todo'),
    # todo更新
    path('update/<int:pk>', views.TodoCreateView.as_view(), name='update-todo'),
]

from . import views
from django.urls import path, include


urlpatterns = [
    # todo追加
    path('addtodo/', views.TodoCreateView.as_view(), name='add-todo'),
]

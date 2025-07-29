from . import views
from django.urls import path, include


urlpatterns = [
    # 新規登録処理'
    path('signup/', views.RegisterView.as_view(), name='user-signup'),
    # ログイン'
    path('login/', views.LoginView.as_view(), name='user-login'),
    #プロフィール取得
    path('getuser/', views.GetProfileView.as_view(), name='get-userprofile'),
    #トークン取得
    path('gettoken/', views.GetTokenView.as_view(), name='get-token'),
]

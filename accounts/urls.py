from . import views
from django.urls import path, include


urlpatterns = [
    path('signup/', views.RegisterView.as_view(), name='user-signup'), # 新規登録処理'
    path('login/', views.LoginView.as_view(), name='user-login'), # ログイン'
    path('getuser/', views.GetProfileView.as_view(), name='get-userprofile'), #プロフィール取得
    path('gettoken/', views.GetTokenView.as_view(), name='get-token'), #トークン取得
]

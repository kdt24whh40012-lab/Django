from django.urls import path
from . import views

app_name = 'psys'

urlpatterns = [
    path('CustomerSerch/', views.CustomerSearch, name='CustomerSearch'),
    # ログイン用のパスを追加（例）
    path('login/', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
]
from django.urls import path, re_path
from user import views


urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    re_path('set_password/(\w+)/', views.set_password, name='set_password'),
]

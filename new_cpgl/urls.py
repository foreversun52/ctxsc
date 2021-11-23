from new_cpgl import settings
from django.contrib import admin
from django.views.static import serve
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('home/',include('home.urls')),
    path('main/',include('main.urls')),
    # 暴露给外界的后端文件资源
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
]

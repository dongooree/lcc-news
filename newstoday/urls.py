"""newstoday URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
# from .views import * # 루트 디렉토리의 views에서 모든 함수를 가져온다.
# djangoMaster>views.py에서 모든 함수를 가져온다.

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.main), # views.py의 main함수를 의미한다.
    path('crawling_today_cs/', views.crawling_today_cs, name="cs"),
]


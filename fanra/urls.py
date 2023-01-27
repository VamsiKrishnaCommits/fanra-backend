"""fanra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from fanra.views import FetchRelationShip

from fanra.views import FetchCelebs
from fanra.views import Fetchbuild
fetch_celebs = FetchCelebs.as_view({"get": "list"})
fetch_relation = FetchRelationShip.as_view({'get':'retrieve'})
test_build_graph=Fetchbuild.as_view({'get':'retrieve'})
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/fetch", fetch_celebs),
    path('api/v1/fetch_relation' , fetch_relation),
    path('api/v1/build_graph' , test_build_graph)

]

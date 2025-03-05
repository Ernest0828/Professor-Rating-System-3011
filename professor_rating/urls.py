"""
URL configuration for professor_rating project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from ratings.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('view_mod/', view), #show modules
    path('view_professor/', view_professor), #show professors
    path('view_rating/', view_rating), #show ratings
    path('view_mod_instance/', view_module_instance), #show module instances
    path('view_cached_rating/', view_cached_rating), #show cached ratings
    path('register/', register_view), #1.register user
    path('login/', login_view), #2.login user
    path('logout/', logout_view), #3.logout user
    path('list/', list_view), #4.list all modules
    path('view/', rating_view), #5.list all professors
    path('average/', average_view), #6.average rating for professor
    path('rate/', rate_view), #7.rate a professor
]

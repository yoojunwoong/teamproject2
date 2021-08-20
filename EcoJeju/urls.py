"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

from EcoJeju import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('userboard', views.userboard, name="userboard"),
    path('workerboard', views.workerboard, name="workerboard"),

    path('login', views.login, name="login"),
    path('loginimpl', views.loginimpl, name='loginimpl'),

    path('register', views.register, name="register"),
    path('registerimpl', views.registerimpl, name='registerimpl'),

    path('recover',views.recover, name="recover"),

    path('card1', views.card1, name="card1"),
    path('card2', views.card2, name="card2"),

    path('plot1', views.plot1, name="plot1"),
    path('plot3', views.plot3, name="plot3"),

    path('usergimpl', views.usergimpl, name="usergimpl"),
    path('bars3', views.bars3, name="bars3"),
    path('bars4', views.bars4, name="bars4"),

    path('piecharts', views.piecharts, name="piecharts"),
    path('tables',views.tables, name="tables"),
    path('insertdata', views.insertdata, name="insertdata"),
    path('into', views.into, name="into"),

]

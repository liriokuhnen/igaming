from django.urls import path

from . import views

urlpatterns = [
    path('', views.indexView, name='index'),
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('signup', views.signUpView, name='signUp'),
    path('home', views.homeView, name='home'),
    path('deposit', views.depositView, name='deposit'),
    path('game/spin', views.spinGameView, name='spinGame'),
]
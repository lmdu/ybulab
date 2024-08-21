from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name='index'),
	path('login', views.login, name='login'),
	path('register', views.register, name='register'),
	path('reset', views.reset, name='reset'),
	path('validate', views.validate, name='validate'),
]
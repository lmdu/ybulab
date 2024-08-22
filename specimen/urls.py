from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name='index'),
	path('signin', views.signin, name='signin'),
	path('signup', views.signup, name='signup'),
	path('signout', views.signout, name='signout'),
	path('reset', views.reset, name='reset'),
	path('validate', views.validate, name='validate'),
	path('sample/<action>', views.sample, name='sample'),
]
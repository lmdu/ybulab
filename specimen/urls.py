from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	path("", views.index, name='index'),
	path('signin', views.signin, name='signin'),
	path('signup', views.signup, name='signup'),
	path('signout', views.signout, name='signout'),
	path('validate', views.validate, name='validate'),
	path('upload', views.upload, name='upload'),
	path('species/<action>', views.species, name='species'),
	path('sample/<action>', views.sample, name='sample'),
	path('specimen/<action>', views.specimen, name='specimen'),
	path('customer/<action>', views.customer, name='customer'),
	path('profile/<action>', views.profile, name='profile'),
	path('setpass/<action>', views.setpass, name='setpass'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

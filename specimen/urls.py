from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	path("", views.index, name='index'),
	path('signin', views.signin, name='signin'),
	path('signup', views.signup, name='signup'),
	path('signout', views.signout, name='signout'),
	path('reset', views.reset, name='reset'),
	path('validate', views.validate, name='validate'),
	path('species', views.species, name='species'),
	path('upload', views.upload, name='upload'),
	path('sample/<action>', views.sample, name='sample'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

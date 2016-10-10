from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     url(r'^$', views.profile, name='profile'),
     url(r'^username/', views.usernameEdit, name='username edit'),
     url(r'^email/', views.emailEdit, name='email edit'),
     url(r'^first/', views.firstNameEdit, name='firstname edit'),
     url(r'^last/', views.lastNameEdit, name='lastname edit'),
     url(r'^delete/', views.deleteProfile, name='delete profile'),
  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
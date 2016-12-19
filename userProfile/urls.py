from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     url(r'^$', views.register_user, name='reg'),
     url(r'^profile/', views.profile, name='profile'),
     url(r'^username/', views.usernameEdit, name='username edit'),
     url(r'^email/', views.emailEdit, name='email edit'),
     url(r'^first/', views.firstNameEdit, name='firstname edit'),
     url(r'^last/', views.lastNameEdit, name='lastname edit'),
     url(r'^delete/', views.deleteProfile, name='delete profile'),
     url(r'^login/', views.user_login, name='login'),
     url(r'^logout/', views.user_logout, name='logout'),
     url(r'^success/', views.success, name='register success'),
     url(r'^confirm/', views.confirm, name="email confirm"),
  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
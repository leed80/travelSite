from django.conf.urls import url

from . import views

urlpatterns = [
     url(r'^$', views.register_user, name='reg'),
     url(r'^login/', views.user_login, name='login'),
     url(r'^logout/', views.user_logout, name='logout'),
     url(r'^success/', views.success, name='register success'),
     url(r'^confirm/', views.confirm, name="email confirm"),
     
]



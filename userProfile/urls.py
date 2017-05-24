from django.conf.urls import url

import userProfile.controllers
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     url(r'^registration_page/', userProfile.controllers.registration_page_controller, name='reg page'),
     url(r'^registration/', userProfile.controllers.register_user_controller, name='reg page'),
     url(r'^profile/', userProfile.controllers.profile, name='profile'),
     url(r'^delete/', userProfile.controllers.deleteProfile, name='delete profile'),
     url(r'^login/', userProfile.controllers.user_login, name='login'),
     url(r'^logout/', userProfile.controllers.user_logout, name='logout'),
     url(r'^success/', userProfile.controllers.success, name='register success'),
     # url(r'^confirm/', userProfile.controllers.confirm, name="email confirm"),
  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
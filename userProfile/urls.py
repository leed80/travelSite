from django.conf.urls import url

import userProfile.controllers
from . import views
from django.conf.urls.static import static
from django.conf import settings
import django.contrib.auth.views

urlpatterns = [
     url(r'^registration_page/', userProfile.controllers.registration_page_controller, name='reg page'),
     url(r'^registration/', userProfile.controllers.register_user_controller, name='reg page'),
     url(r'^profile/', userProfile.controllers.profile, name='profile'),
     url(r'^delete/', userProfile.controllers.deleteProfile, name='delete profile'),
     url(r'^logout/', userProfile.controllers.user_logout_controller, name='logout'),
     url(r'^confirm/', userProfile.controllers.activate_account, name="email confirm"),
     url(r'^login/$', django.contrib.auth.views.login, {'template_name': 'reg/login.html'}, name='login'),
     url(r'^edit_details', userProfile.controllers.edit_user_profile_controller, name="edit profile")
  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
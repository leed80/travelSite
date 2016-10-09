from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
     url(r'^$', views.prof, name='profile'),
     url(r'^username/', views.username_edit, name='username_edit'),
     url(r'^email/', views.email_edit, name='email_edit'),
     url(r'^first/', views.first_name_edit, name='firstname_edit'),
     url(r'^last/', views.last_name_edit, name='lastname_edit'),
     url(r'^delete/', views.deleteProfile, name='delete profile'),
  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
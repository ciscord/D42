from django.conf.urls import url
from project import views

legal_patterns = [
  url(r'^privacy/$', views.legal_privacy, name='legal_privacy'),
  url(r'^eula/$', views.legal_eula, name='legal_eula'),
  url(r'^d42_open_disc_eula/$', views.legal_d42_open_disc_eula, name='legal_d42_open_disc_eula'),
]

from django.conf.urls import url
from project import views

partners_patterns = [
    url(r'^$', views.partners, name='partners'),
    url(r'^benefits/$', views.partners_benefits, name='partners_benefits'),
    url(r'^learn-more/$', views.partners_learnmore, name='partners_learnmore'),
    url(r'^register/$', views.partners_register, name='partners_register'),
    url(r'^find/$', views.partners_find, name='partners_find'),
]

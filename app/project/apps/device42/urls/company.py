from django.conf.urls import url
from project import views


company_patterns = [

  url(r'^contact/$', views.company_contact, name='company_contact'),
  url(r'^jobs/$', views.company_jobs, name='company_jobs'),
  url(r'^jobs/devops_evanglist/$', views.company_jobs_devops, name='company_jobs_devops'),
]

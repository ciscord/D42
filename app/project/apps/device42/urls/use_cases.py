from django.conf.urls import url
from project import views

use_case_patterns = [
  url(r'^$', views.use_cases, name='use_cases'),
  url(r'^hardware-audit/$', views.use_cases_hardware_audit, name='use_cases_hardware_audit'),
  url(r'^software-audit-and-compliance/$', views.use_cases_software_audit_and_compliance,
      name='use_cases_software_audit'),
  url(r'^data-center-and-cloud-migration/$', views.use_cases_data_center_and_cloud_migration,
      name='use_cases_data_center_and_cloud_migration'),
  url(r'^budgeting-and-finance/$', views.use_cases_budgeting_and_finance, name='use_cases_budgeting_and_finance'),
  url(r'^it-agility/$', views.use_cases_it_agility, name='use_cases_it_agility'),
  url(r'^security-and-compliance/$', views.use_cases_security_and_compliance, name='use_cases_security_and_compliance'),
  url(r'^capacity-planning/$', views.use_cases_capacity_planning, name='use_cases_capacity_planning'),
  url(r'^it-automation/$', views.use_cases_it_automation, name='use_cases_it_automation'),
  url(r'^mergers-and-acquisitions/$', views.use_cases_mergers_and_acquisitions,
      name='use_cases_mergers_and_acquisitions'),
  url(r'^os-migration/$', views.use_cases_migrations, name='use_cases_migrations'),
]

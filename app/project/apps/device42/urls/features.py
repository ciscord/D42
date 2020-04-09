from django.conf.urls import url
from django.views.generic.base import RedirectView
from project import views


features_patterns = [
  url(r'^$', views.features, name="features"),
  url(r'^data-center-management/$', views.features_dcim, name='features_dcim'),
  url(r'^it-asset-management/$', views.features_itam, name='features_itam'),
  url(r'^ip-address-management/$', views.features_ipam, name='features_ipam'),
  url(r'^device-discovery/$', views.features_discovery, name='features_discovery'),
  url(r'^role-based-access/$', views.features_role_based_access, name='features_role_based_access'),
  url(r'^application-mappings/$', views.features_app_mapping, name='features_app_mapping'),
  url(r'^software-license-management/$', views.features_software_license, name='features_software_license'),
  url(r'^enterprise-password-management/$', views.features_password_management, name='features_password_management'),
  url(r'^cmdb/$', views.features_cmdb_for_cloud_era, name='features_cmdb_for_cloud_era'),
  url(r'^integrations/$', views.features_integrations, name='features_integrations'),
  #
  #  redirects
  url(r'^password_management/$', RedirectView.as_view(url='/features/enterprise-password-management/')),
  url(r'^data_center_management/$', RedirectView.as_view(url='/features/data-center-management/')),
  url(r'^auto-discovery/$', RedirectView.as_view(url='/features/device-discovery/')),
  url(r'^ip_address_management/$', RedirectView.as_view(url='/features/ip-address-management/')),
  url(r'^password-management/$', RedirectView.as_view(url='/features/enterprise-password-management/')),
]

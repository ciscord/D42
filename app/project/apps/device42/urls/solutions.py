from django.conf.urls import url
from project import views


solution_patterns = [
  url(r'^patch-panel-cable-management/$', views.solutions_cable_management, name='solutions_cable_management'),
  url(r'^it-inventory-management/$', views.solutions_it_inventory_management, name='solutions_it_management_software'),
  url(r'^data-center-power-management/$', views.solutions_data_center_power_management, name='solutions_data_center_power_management'),
  url(r'^ip-address-tracking/$', views.solutions_ip_address_tracking_software, name='solutions_data_center_power_management'),
]

from django.conf.urls import url
import project.views as views

videos_patterns = [
  url(r'^$', views.videos, name="videos"),
  url(r'^server-rooms/$', views.videos_server_room, name="videos_server_room"),
  url(r'^enterprise-password-management/$', views.videos_enterprise_password_management, name="videos_enterprise_password_management"),
  url(r'^autodiscovery/$', views.videos_autodiscovery, name="videos_autodiscovery"),
  url(r'^ip-address-management/$', views.videos_ip_address_management, name="videos_ip_address_management"),
  url(r'^patch-panel-management/$', views.videos_patch_panel_management, name="videos_patch_panel_management"),
  url(r'^dcim-demo/$', views.videos_dcim_demo, name="videos_dcim_demo"),
  url(r'^managing-racks/$', views.videos_rack_management, name="videos_rack_management"),
  url(r'^basic-navigation/$', views.videos_basic_navigation, name="videos_basic_navigation"),
  url(r'^hierarchy/$', views.videos_hierarchy, name="videos_hierarchy"),
  url(r'^introduction/$', views.videos_introduction, name="videos_introduction"),
]

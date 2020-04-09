from django.conf.urls import url
from project import views

vs_patterns = [
  url(r'^$', views.compare, name='compare'),
  url(r'^nlyte/$', views.compare_nlyte, name='compare_nlyte'),
  url(r'^servicenow/$', views.compare_servicenow, name='compare_servicenow'),
  url(r'^bmc-atrium/$', views.compare_bmc_atrium, name='compare_bmc_atrium'),
  url(r'^hp-ucmdb/$', views.compare_hp_ucmdb, name='compare_hp_ucmdb'),
  url(r'^solarwinds/$', views.compare_solarwinds, name='compare_solarwinds'),
  url(r'^sunbird/$', views.compare_sunbird, name='compare_sunbird'),
  url(r'^infoblox/$', views.compare_infoblox, name='compare_infoblox'),
  url(r'^risc-networks/$', views.compare_risc, name='compare_risc'),
  url(r'^bmc-discovery/$', views.compare_bmc_discovery, name='compare_bmc_discovery'),
]

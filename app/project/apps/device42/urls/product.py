from django.conf.urls import url
from project import views


product_patterns = [
  url(r'^$', views.product, name='product'),
  url(r'^benefits/$', views.product_benefits, name='product_benefits'),
  url(r'^pricing/$', views.product_pricing, name='product_pricing'),
]

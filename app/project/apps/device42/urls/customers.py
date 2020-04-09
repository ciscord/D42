from django.conf.urls import url
from project import views


customers_patterns = [
  url(r'^$', views.customers, name="customers"),
  url(r'^testimonials/$', views.customers_testimonials,
      name="customers_testimonials"),
  url(r'^social/$', views.customers_social_mentions,
      name="customers_social_mentions"),
  url(r'^case-studies/$', views.customers_case_studies,
      name="customers_case_studies"),
  url(r'^case-studies/intl-financial-service-provider/$',
      views.case_studies_intl_financial_service_provider,
      name="case_studies_intl_financial_service_provider"),
  url(r'^case-studies/coventry-university/$',
      views.case_studies_coventry_university, name="case_studies_conventry_university"),
  url(r'^case-studies/maxihost/$', views.case_studies_maxihost,
      name="case_studies_maxihost"),
]

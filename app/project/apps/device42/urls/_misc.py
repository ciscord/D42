from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from project import views

redirects_patterns = i18n_patterns(
  # REDIRECT OLD URLS (returns 301 - seo safe)

  prefix_default_language=False
)

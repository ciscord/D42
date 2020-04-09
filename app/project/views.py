import pytz, uuid, time, json
from django import forms as forms
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.template import Context
from django.views.decorators.cache import never_cache, cache_page
from django.utils.translation import ugettext as _, get_language
from django.views.i18n import javascript_catalog
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.http import Http404, JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.views import View
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from project.apps.device42 import models, view_logic, forms
from project.apps.device42.incognitos import INCOGNITO_LIST


class DirectTemplateView(TemplateView):
  extra_context = None

  def get_context_data(self, **kwargs):
    context = super(self.__class__, self).get_context_data(**kwargs)
    if self.extra_context is not None:
      for key, value in self.extra_context.items():
        if callable(value):
          context[key] = value()
        else:
          context[key] = value
    return context


@cache_page(86400, key_prefix='js18n')
def cached_javascript_catalog(request, domain='djangojs', packages=None):
  from django.views.i18n import javascript_catalog
  return javascript_catalog(request, domain, packages)


def home(request):
  import feedparser

  BLOG_FEED = feedparser.parse('http://www.device42.com/blog/feed')
  LOGOS = _getClientLogos
  return render(request, 'home.html', {"logos": LOGOS, "blog_feed": BLOG_FEED})


def error404(request):
  return render(request, '404.html')


@never_cache
def thanks(request, id=9):
  if not id or id is 9:
    return home(request)
  if 'temp_data' in request.session:
    return render(request, 'forms/thank-you.html', {'id': id, 'the_data': request.session['temp_data']})
  else:
    return render(request, 'forms/thank-you.html', {'id': id})


def faq_sales(request):
  return render(request, 'sections/product/faq_sales.html')


def faq_power(request):
  return render(request, 'sections/product/faq_power.html')


@never_cache
def schedule_form(request):
  if request.method == 'POST':
    if request.POST['main'] == '':
      form = forms.ScheduleForm(request.POST)
      if form.is_valid():

        fc = form.save(commit=False)
        the_ref = request.META.get('HTTP_REFERER', None)
        the_cookie = request.COOKIES.get('hubspotutk', None)
        fc.clicky_cookie = request.COOKIES.get('_jsuid', '')
        fc.intercom_id = request.COOKIES.get('intercom-id', '')
        fc.ip_address = client_address = request.META.get('REMOTE_ADDR', '')
        fc.save()

        name = form.cleaned_data['name']
        phone = form.cleaned_data['phone']
        sender = form.cleaned_data['email']

        message2 = """
        Name: %s
        Email: %s
        Phone: %s
        IP: %s
        """ % (name, sender, phone, client_address)
        from_address = ['support@device42.com']
        recipients = ['scanelli@device42.com', 'al.rossini@device42.com', ]  # 'raj@rajlog.com',
        if settings.DEBUG:
          recipients = ['dave.amato@device42.com', ]
        subject = "FYI: online demo - already sent an invite "

        send_mail(subject, message2, from_address, recipients)
        if not settings.DEBUG:
          view_logic.immediate_schedule_demo_send(name, sender)
          view_logic.hubspot_data_send('schedule_demo', the_cookie, client_address, the_ref, form.cleaned_data['name'],
                                       form.cleaned_data['email'], None, None, None, form.cleaned_data['phone'])

        request.session['temp_data'] = form.cleaned_data
        return redirect(resolve_url('/thanks/0/'))
    else:
      if settings.DEBUG:
        send_to = ['dave.amato@device42.com', ]
      else:
        send_to = ['raj@rajlog.com', ]
      send_mail('demo -ve', str(request.POST), 'support@device42.com', send_to)
      return redirect(resolve_url('/thanks/0/'))
  else:
    form = forms.ScheduleForm()
  return render(request, 'forms/schedule_demo.html', {'form': form})


def customers(request):
  CLIENT_LOGOS = _getClientLogos()
  return render(request, 'sections/customers/_customers.html', {'logos': CLIENT_LOGOS, })


def customers_testimonials(request):
  return render(request, 'sections/customers/testimonials.html')


def customers_social_mentions(request):
  return render(request, 'sections/customers/social-mentions.html')


def customers_case_studies(request):
  return render(request, 'sections/customers/case-studies.html')


def case_studies_intl_financial_service_provider(request):
  return render(request, 'sections/customers/_intl-financial-service-provider.html')


def case_studies_coventry_university(request):
  return render(request, 'sections/customers/_coventry-university.html')


def case_studies_maxihost(request):
  return render(request, 'sections/customers/_maxihost-data-center.html')


def legal_d42_open_disc_eula(request):
  return render(request, 'sections/legal/d42_open_disc_eula.html')


def legal_eula(request):
  return render(request, 'sections/legal/eula.html')


def legal_privacy(request):
  return render(request, 'sections/legal/privacy.html')


def product(request):
  return redirect('/')


def product_benefits(request):
  return render(request, 'sections/product/benefits.html')


@never_cache
def product_pricing(request):
  return render(request, 'sections/product/pricing.html')


def use_cases(request):
  return render(request, 'sections/product/_use-cases.html')


def use_cases_budgeting_and_finance(request):
  return render(request, 'sections/product/use-cases/budgeting-and-finance.html')


def use_cases_capacity_planning(request):
  return render(request, 'sections/product/use-cases/capacity-planning.html')


def use_cases_data_center_and_cloud_migration(request):
  return render(request, 'sections/product/use-cases/data-center-and-cloud-migration.html')


def use_cases_hardware_audit(request):
  return render(request, 'sections/product/use-cases/hardware-audit.html')


def use_cases_it_agility(request):
  return render(request, 'sections/product/use-cases/it-agility.html')


def use_cases_it_automation(request):
  return render(request, 'sections/product/use-cases/it-automation.html')


def use_cases_mergers_and_acquisitions(request):
  return render(request, 'sections/product/use-cases/mergers-and-acquisitions.html')


def use_cases_migrations(request):
  return render(request, 'sections/product/use-cases/migrations.html')


def use_cases_software_audit_and_compliance(request):
  return render(request, 'sections/product/use-cases/software-audit-and-compliance.html')


def use_cases_security_and_compliance(request):
  return render(request, 'sections/product/use-cases/security-and-compliance.html')


@never_cache
def pricing(request):
  client_address = ''
  bot = False
  show_price = False
  if 'HTTP_USER_AGENT' in request.META:
    is_it_bot = view_logic.parse_user_agent(request.META.get('HTTP_USER_AGENT'))
    bot = True
    if not is_it_bot:
      if 'REMOTE_ADDR' in request.META:
        client_address = request.META['REMOTE_ADDR']
  if client_address:
    continent, country = view_logic.get_ip_data(client_address)
    if continent and str(continent) != 'AS':
      show_price = True
    elif country and str(country) == 'JP':
      show_price = True
  else:
    if not bot:
      boyd = 'no client  ip found, here is meta ' + request.META
      send_mail('pricing page no ip', boyd, 'support@device42.com', ['raj@rajlog.com', 'dave.amato@device42.com', ])
  if show_price:
    return render(request, 'pricing.html')
  else:
    # form processing code goes here
    if request.method == 'POST':  # If the form has been submitted...
      form = PricingContactForm(request.POST)  # A form bound to the POST data
      if form.is_valid():  # All validation rules pass
        # Process the data in form.cleaned_data
        # ...
        fc = form.save(commit=False)
        client_address = ''
        if 'HTTP_REFERER' in request.META:
          the_ref = request.META['HTTP_REFERER']
        else:
          the_ref = None
        if 'REMOTE_ADDR' in request.META:
          client_address = request.META['REMOTE_ADDR']
        if 'hubspotutk' in request.COOKIES:
          the_cookie = request.COOKIES['hubspotutk']
        else:
          the_cookie = None
        fc.ip_address = client_address
        fc.save()
        message2 = json.dumps(form.cleaned_data, indent=2)
        from_address = 'support@device42.com'
        recipients = ['raj@rajlog.com', 'sales@device42.com']  # 'scanelli@device42.com']
        subject = 'Pricing Page Form'
        now = datetime.now()
        if settings.DEBUG:
          subject = '[testing] Pricing Page Form'
          recipients = ['dave.amato@device42.com', 'raj@rajlog.com']
        if request.POST['address'] == '':
          email_body = '<html><head></head><body>' \
                       '<table width="500" cellpadding="3px" cellspacing="0" align="center">'
          for key in form.cleaned_data:
            email_body += '<tr><td style="border:1px solid #444444;padding:3px;" width="245"><b>' + form.fields[
              key].label + '</b></td><td style="border:1px solid #444444;padding:3px;" width="245">'
            if form.fields[key].__class__.__name__ == 'BooleanField':
              if form.cleaned_data.get(key):
                email_body += 'Yes'
              else:
                email_body += 'No'
            elif key == 'device_count':
              email_body += request.POST.get('id_device_count', '--')
            else:
              email_body += form.cleaned_data.get(key)
            email_body += '</td></tr>'
          email_body += '<tr><td style="padding:3px;" width="245"><b>Submission Time</b></td><td style="padding:3px;" width="245">'
          email_body += now.strftime("%m-%d-%Y %I:%M%p")
          email_body += '</td></tr></table></body></html>'
          send_mail(subject, email_body, from_address, recipients)
        else:
          send_email('prcing -ve', message2, from_address, ['raj@rajlog.com'])
        request.session['temp_data'] = form.cleaned_data
        return HttpResponseRedirect(translation.get_language() + '/thanks/0/')  # Redirect after POST
    else:
      form = PricingContactForm()  # An unbound form
    return render(request, "nopricing.html", {'form': form})


def features(request):
  return render(request, 'sections/features/_features.html')


def features_dcim(request):
  return render(request, 'sections/features/data-center-management.html')


def features_itam(request):
  return render(request, 'sections/features/it-asset-management.html')


def features_ipam(request):
  return render(request, 'sections/features/ip-address-management.html')


def features_discovery(request):
  return render(request, 'sections/features/device-discovery.html')


def features_role_based_access(request):
  return render(request, 'sections/features/role-based-access.html')


def features_app_mapping(request):
  return render(request, 'sections/features/application-mapping.html')


def features_software_license(request):
  return render(request, 'sections/features/software-license-management.html')


def features_password_management(request):
  return render(request, 'sections/features/password-management.html')


def features_cmdb_for_cloud_era(request):
  return render(request, 'sections/features/cmdb-for-cloud-era.html')

def features_integrations(request):
  return render(request, 'sections/features/integrations.html')

def company(request):
  return render(request, 'sections/company/_company.html', {'include_company_info': True})


def company_about(request):
  return company(request)


def company_jobs(request):
  return render(request, 'sections/company/jobs.html', {'jobs': _getJobs()})


def company_jobs_devops(request):
  return render(request, 'sections/company/jobs_devops.html', {'jobs': _getJobs()})


def company_contact(request):
  form = forms.ContactForm()
  if request.method == 'POST':
    form = forms.ContactForm(request.POST)
    if form.is_valid():
      fc = form.save(commit=False)
      client_address = clicky_cookie = ''
      if 'HTTP_REFERER' in request.META: the_ref = request.META['HTTP_REFERER']
      else: the_ref = None
      if 'REMOTE_ADDR' in request.META: client_address = request.META['REMOTE_ADDR']
      if 'hubspotutk' in request.COOKIES: the_cookie = request.COOKIES['hubspotutk']
      else: the_cookie = None
      if '_jsuid' in request.COOKIES: clicky_cookie = request.COOKIES['_jsuid']

      fc.ip_address = client_address
      fc.clicky_cookie = clicky_cookie

      name = form.cleaned_data['name']
      subject = form.cleaned_data['topic']
      message = form.cleaned_data['message']
      sender = form.cleaned_data['email']
      phone = form.cleaned_data['phone']


      message2 = """
Contact Form Submission

Name: %s
Sender: %s
Phone: %s
Topic: %s
Message: %s
IP: %s
""" % (name, sender, phone, subject, message, client_address)
      from_address = 'support@device42.com'
      recipients = ['raj@rajlog.com', 'scanelli@device42.com']
      if settings.DEBUG:
        recipients = ['dave.amato@device42.com']
      if request.POST['address'] == '':
        fc.save()
        send_mail('Contact Form', message2, from_address, recipients)
        view_logic.hubspot_data_send('contact', the_cookie, client_address, the_ref, form.cleaned_data['name'],
                          form.cleaned_data['email'], form.cleaned_data['topic'], form.cleaned_data['message'],
                          form.cleaned_data['phone'], form.cleaned_data['phone'])
      else:
        send_mail('contact -ve', message2, from_address, ['raj@rajlog.com', 'dave.amato@device42.com'])
      request.session['temp_data'] = form.cleaned_data
      return redirect(resolve_url('/thanks/0/'))
    else:
      pass
  return render(request, 'sections/company/contact.html', {'form': form})


@never_cache
def download(request):
  the_matrix = {'name': '',
                'email': '',
                'vp': '',
                'eula': False,
                'name_error': False,
                'email_error': False,
                'platform_error': False,
                'eula_error': False,
                'errors': False,
                }
  if request.method == 'POST':
    if request.POST['main'] == '':
      form = forms.DownloadForm(request.POST)
      if form.is_valid():
        the_ref = client_address = clicky_cookie = intercom_id = the_cookie = ''
        if 'HTTP_REFERER' in request.META:
          the_ref = request.META['HTTP_REFERER']
        else:
          the_ref = None
        if 'REMOTE_ADDR' in request.META: client_address = request.META['REMOTE_ADDR']
        if 'hubspotutk' in request.COOKIES: the_cookie = request.COOKIES['hubspotutk']
        if '_jsuid' in request.COOKIES: clicky_cookie = request.COOKIES['_jsuid']
        if 'intercom-id' in request.COOKIES:
          intercom_id = request.COOKIES['intercom-id']

        download_uuid = str(uuid.uuid1())
        email_clean = form.cleaned_data['email']
        name_clean = form.cleaned_data['name']
        dwnld = models.DownloadModel.objects.create(name=name_clean, email=email_clean,
                                                    I_agree_to_EULA=True, ip_address=client_address,
                                                    download_uuid=download_uuid, clicky_cookie=clicky_cookie, )
        subject = 'Download'
        message2 = """
Download Form Submission

Name: %s
Sender: %s
Client IP: %s
""" % (name_clean, email_clean, client_address)

        from_address = 'support@device42.com'
        recipients = ['raj@rajlog.com']
        if settings.DEBUG:
          recipients = ['dave.amato@device42.com', ]
        view_logic.immediate_download_send(request, name_clean, email_clean, download_uuid)
        send_mail(subject, message2, from_address, recipients)
        view_logic.hubspot_data_send('download', the_cookie, client_address, the_ref, name_clean,
                                     email_clean, '')
        request.session['temp_data'] = form.cleaned_data

      else:
        return render(request, 'forms/download.html', {'form': form})
    else:
      send_mail('download -ve', str(request.POST), 'support@device42.com', ['raj@rajlog.com'])
    return redirect(resolve_url('/thanks/1/'))
  else:
    form = forms.DownloadForm()
  return render(request, 'forms/download.html', {'form': form})


@never_cache
def download_links(request, download_uuid):
  dwnld = models.DownloadModel.objects.filter(download_uuid=download_uuid)
  the_links = []
  error_message = ""
  form = forms.DownloadForm()
  if (dwnld.count() == 1):
    links = models.DownloadLinks.objects.filter(downloadmodel=dwnld[0])
    atime = time.mktime(dwnld[0].time_linked.timetuple())
    expires = int(atime) + 7 * 24 * 60 * 60
    if int(time.time()) > expires:
      error_message = _("Your download link has expired")
    elif len(links) == 0:
      the_links = view_logic.generate_download_links(expires)
      for _dict in the_links:
        models.DownloadLinks.objects.create(name=_dict['name'], link=_dict['link'], size=_dict['size'],
                                            downloadmodel=dwnld[0],
                                            img_src=_dict['img_src'])
    else:
      for link in links:
        the_links.append({'name': link.name, 'link': link.link, 'size': link.size, 'img_src': link.img_src})
  else:
    error_message = _("Could not find your download link")
    the_matrix = {'name': '',
                  'email': '',
                  'vp': '',
                  'eula': False,
                  'name_error': False,
                  'email_error': False,
                  'platform_error': False,
                  'eula_error': False,
                  'errors': False,
                  }
    if request.method == 'POST':
      if request.POST['main'] == '':
        form = forms.DownloadForm(request.POST)
        if form.is_valid():
          the_ref = client_address = clicky_cookie = intercom_id = the_cookie = ''
          if 'HTTP_REFERER' in request.META:
            the_ref = request.META['HTTP_REFERER']
          else:
            the_ref = None
          if 'REMOTE_ADDR' in request.META: client_address = request.META['REMOTE_ADDR']
          if 'hubspotutk' in request.COOKIES: the_cookie = request.COOKIES['hubspotutk']
          if '_jsuid' in request.COOKIES: clicky_cookie = request.COOKIES['_jsuid']
          if 'intercom-id' in request.COOKIES:
            intercom_id = request.COOKIES['intercom-id']
          else:
            the_cookie = None

          download_uuid = str(uuid.uuid1())
          email_clean = form.cleaned_data['email']
          name_clean = form.cleaned_data['name']
          dwnld = models.DownloadModel.objects.create(name=name_clean, email=email_clean,
                                                      I_agree_to_EULA=True, ip_address=client_address,
                                                      download_uuid=download_uuid, clicky_cookie=clicky_cookie, )
          subject = 'Download'
          message2 = """Download Form Submission
      Name: %s
      Sender: %s
      Client IP: %s
            """ % (name_clean, email_clean, client_address)

          from_address = 'support@device42.com'
          recipients = ['raj@rajlog.com']
          if settings.DEBUG:
            recipients = ['dave.amato@device42.com', ]
          view_logic.immediate_download_send(request, name_clean, email_clean, download_uuid)
          send_mail(subject, message2, from_address, recipients)
          view_logic.hubspot_data_send('download', the_cookie, client_address, the_ref, name_clean,
                                       email_clean, '')
        else:
          return render(request, 'sections/download_links.html', {'error_message': error_message, 'the_links': the_links,'form': form})
      else:
        send_mail('download -ve', str(request.POST), 'support@device42.com', ['raj@rajlog.com'])
      return redirect(resolve_url('/thanks/1/'))
    else:
      form = forms.DownloadForm()
  return render(request, 'sections/download_links.html', {'error_message': error_message, 'the_links': the_links, 'form': form})


def compare(request):
  return render(request, 'sections/compare/_compare.html')


def compare_nlyte(request):
  return render(request, 'sections/compare/nlyte.html')


def compare_sunbird(request):
  return render(request, 'sections/compare/sunbird.html')


def compare_servicenow(request):
  return render(request, 'sections/compare/servicenow.html')


def compare_bmc_atrium(request):
  return render(request, 'sections/compare/bmc-atrium.html')


def compare_hp_ucmdb(request):
  return render(request, 'sections/compare/hp-ucmdb.html')


def compare_solarwinds(request):
  return render(request, 'sections/compare/solarwinds.html')


def compare_infoblox(request):
  return render(request, 'sections/compare/infoblox.html')


def compare_dcim(request):
  return render(request, 'sections/compare/dcim.html')


def compare_ipam(request):
  return render(request, 'sections/compare/ipam.html')


def compare_cmdb(request):
  return render(request, 'sections/compare/cmdb.html')


def compare_risc(request):
  return render(request, 'sections/compare/risc.html')

def compare_bmc_discovery(request):
  return render(request, 'sections/compare/bmc-discovery.html')


def videos(request):
  return render(request, 'sections/support/_videos.html', {'videos': _getVideos()})

def videos_introduction(request):
  return render(request, 'sections/support/videos/introduction.html')

def videos_dcim_demo(request):
  return render(request, 'sections/support/videos/quick-demo.html')


def videos_server_room(request):
  return render(request, 'sections/support/videos/server-rooms.html')


def videos_basic_navigation(request):
  return render(request, 'sections/support/videos/basic-navigation.html')


def videos_rack_management(request):
  return render(request, 'sections/support/videos/rack-management.html')


def videos_patch_panel_management(request):
  return render(request, 'sections/support/videos/patch-panel-management.html')


def videos_ip_address_management(request):
  return render(request, 'sections/support/videos/ip-address-management.html')


def videos_hierarchy(request):
  return render(request, 'sections/support/videos/hierarchy.html')


def videos_enterprise_password_management(request):
  return render(request, 'sections/support/videos/enterprise-password-management.html')


def videos_autodiscovery(request):
  return render(request, 'sections/support/videos/autodiscovery.html')


def opensource(request):
  return render(request, 'sections/support/opensource.html')


def software(request):
  utilities = _getUtilities()
  return render(request, 'sections/support/_software.html', {'tools': utilities})


@never_cache
def software_detail(request, package):
  utilities = _getUtilities()
  if package in utilities.values():
    if (request.method == 'POST') and ('download' in request.POST):
      _download = request.POST.get('download')
      if ('open disc' in _download):
        form = forms.FreeClientForm(request.POST)
        if form.is_valid() and ('main' in request.POST):
          link = view_logic.generate_link_software(package, request, form)
          return HttpResponseRedirect(link)
      elif ('update' in _download):
        form = forms.UpdateForm(request.POST)
        if ('pma' in _download):
          update_type = 'pma'
        else:
          update_type = 'regular'

        if form.is_valid() and (request.POST['main'] == ''):
          link = view_logic.generate_link_software(package, request, form)
          return HttpResponseRedirect(link)
        else:
          return render(request, 'sections/support/_software.html',
                        {'tools': utilities, 'package': package, 'error': update_type})
      else:
        if 'main' in request.POST:
          link = view_logic.generate_link_software(package, request)
          return HttpResponseRedirect(link)
        else:
          # return render(request, 'sections/support/_software.html',
          #               {'tools': utilities, 'package': package})
          if 'main' in request.POST:
            link = view_logic.generate_link_software(package, request)
            return HttpResponseRedirect(link)
          else:
            return render(request, 'sections/support/_software.html', {'tools': utilities, 'package': package})
    else:
      return render(request, 'sections/support/_software.html', {'tools': utilities, 'package': package})
  else:
    return HttpResponseRedirect(reverse('software'))


def integrations(request):
  integrations_object = _getIntegrations()
  integrations_detail = _getIntegrationDetails()

  return render(request, 'sections/support/_integrations.html',
                {'integrations': integrations_object, 'integration_details': integrations_detail})


@never_cache
def integrations_detail(request, slug):
  integrations_object = _getIntegrations()

  if slug in integrations_object.values():
    if request.method == 'POST':
      if slug == "service-now":
        link = "https://api.github.com/repos/device42/servicenow_device42_mapping/zipball"
      elif slug == "servicenow-express":
        link = "https://api.github.com/repos/device42/device42_to_servicenow_express/zipball"
      elif slug == "rundeck":
        link = view_logic.generate_link_generic('d42rundesk-node-1.0.0.jar')
      elif slug == "bmc-remedy":
        link = view_logic.generate_link_generic('d42-bmc_v1.1.zip')
      else:
        return HttpResponseRedirect(reverse('integrations'))

      client_address = clicky_cookie = intercom_id = ''
      if 'REMOTE_ADDR' in request.META: client_address = request.META['REMOTE_ADDR']
      if '_jsuid' in request.COOKIES: clicky_cookie = request.COOKIES['_jsuid']
      if 'intercom-id' in request.COOKIES: intercom_id = request.COOKIES['intercom-id']
      # if clicky_cookie: OtherDownloads.objects.create(type='integrations detail', ip_address=client_address,
      #                                                 clicky_cookie=clicky_cookie, intercom_id=intercom_id)
      return HttpResponseRedirect(link)
    return render(request, 'sections/support/_integrations.html', {'integrations': integrations_object, 'slug': slug})
  else:
    return HttpResponseRedirect(reverse('integrations'))


def migrations(request):
  migrations = _getMigrations()
  return render(request, 'sections/support/_migrations.html', {'migrations': migrations})


def support(request):
  return render(request, 'sections/support/support.html')


@never_cache
def migrations_detail(request, product):
  migrations = _getMigrations()
  response_data = {}
  response_data['status'] = 'ko'

  if product in migrations.values():
    if request.is_ajax():
      try:
        if product == "aperture":
          link = view_logic.generate_link_generic('Aperture-Views_D42-Migration.zip')
        elif product == "opendcim":
          link = "https://github.com/device42/OpenDCIM-to-Device42-Migration/archive/master.zip"
        elif product == "rackmonkey":
          link = "https://github.com/device42/Racktables-to-Device42-Migration/archive/master.zip"
        elif product == "racktables":
          link = "https://github.com/device42/Racktables-to-Device42-Migration/archive/master.zip"
        elif product == "solarwinds-ipam":
          link = "https://github.com/device42/SW_IPAM_to_Device42_Migration/archive/master.zip"

        client_address = request.META.get('REMOTE_ADDR')
        clicky_cookie = request.COOKIES.get('_jsuid')
        intercom_id = request.COOKIES.get('intercom-id')
        if clicky_cookie: models.OtherDownloads.objects.create(type=('%s migration script' % product),
                                                               ip_address=client_address,
                                                               clicky_cookie=clicky_cookie, intercom_id=intercom_id)
        response_data['status'] = 'ok'
        response_data['link'] = link
        return JsonResponse(response_data)
      except:
        response_data['status'] = 'ko'
        response_data['error'] = 'error retrieving download link'
    return render(request, 'sections/support/_migrations.html', {'migrations': migrations, 'product': product})
  else:
    return HttpResponseRedirect(reverse('migrations'))


def partners(request):
  return render(request, 'sections/partners/_partners.html')


def partners_benefits(request):
  return render(request, 'sections/partners/partners_benefits.html')


def partners_learnmore(request):
  return render(request, 'sections/partners/partners_learnmore.html')


def partners_register(request):
  return render(request, 'sections/partners/partners_register.html')


def partners_find(request):
  return render(request, 'sections/partners/partners_find.html')


def tours(request):
  return render(request, 'sections/tours/_tours.html')


def tours_patch_cable_management(request):
  return render(request, 'sections/tours/cable-management.html')


def tours_it_inventory_management(request):
  return render(request, 'sections/tours/it-inventory-management-software.html')


def tours_data_center_power_management(request):
  return render(request, 'sections/tours/data-center-power-management.html')


def tours_ip_address_tracking_software(request):
  return render(request, 'sections/tours/ip-address-tracking-software.html')


def tours_ssl_certificate_management(request):
  return render(request, 'sections/tours/ssl-certificate-management.html', {})


def tours_server_room_management(request):
  return render(request, 'sections/tours/server-room-management.html')


def tours_data_center_documentation(request):
  return render(request, 'sections/tours/data-center-documentation.html')


def tours_history_logs(request):
  return render(request, 'sections/tours/history-logs.html')


def tours_manage_spare_parts(request):
  return render(request, 'sections/tours/manage-spare-parts.html')


def tours_server_inventory(request):
  return render(request, 'sections/tours/server-inventory.html')


def tours_server_rack_diagrams(request):
  return render(request, 'sections/tours/server-rack-diagrams.html')


def roi_calculator(request):
  return render(request, 'components/roi-calculator.html', {})


@never_cache
def offers(request, partner=None):
  if partner and partner in ['metabyte', 'cambridge-computer', 'accudata-systems', 'yandree', ]:
    return render(request, 'base/_base-partner.html', {'partner': partner})
  else:
    raise Http404

def lisa16(request):
  form = None
  if request.method == 'POST':
    form = forms.OtherDownloadsForm(request.POST)

    if form.is_valid():
      client_address = clicky_cookie = intercom_id = ''
      fc = form.save(commit=False)
      if 'REMOTE_ADDR' in request.META: client_address = request.META['REMOTE_ADDR']
      if '_jsuid' in request.COOKIES: clicky_cookie = request.COOKIES['_jsuid']
      if 'intercom-id' in request.COOKIES: intercom_id = request.COOKIES['intercom-id']

      fc.ip_address = client_address
      fc.clicky_cookie = clicky_cookie
      fc.intercom_id = intercom_id
      fc.type = 'lisa16'
      fc.name = name = form.cleaned_data['name']
      fc.email = email = form.cleaned_data['email']
      fc.ip_address = client_address
      fc.save()
      subject = 'LISA16 - Download Request'
      message2 = '''
        LISA Attendee - Download Request
        Name: %s
        Sender: %s
        Client IP: %s
                ''' % (name, email, client_address)
      fc.save()
      from_address = 'support@device42.com'
      recipients = ['sales@device42.com']
      if settings.DEBUG:
        recipients = ['dave.amato@device42.com']
      send_mail(subject, message2, from_address, recipients)
      request.session['temp_data'] = form.cleaned_data
      return thanks(request, id='10')
    else:
      return render(request, 'forms/client_promos/lisa16.html', {'form': form})
  else:
    form = forms.OtherDownloadsForm()

  return render(request, 'forms/client_promos/lisa16.html', {'form': form})



def it_coloring_book(request):
  if request.method == 'POST':
    link = view_logic.generate_link_generic('D42-IT-Adult-Coloring-Book.pdf')
    client_address = clicky_cookie = intercom_id = ''
    if 'REMOTE_ADDR' in request.META: client_address = request.META['REMOTE_ADDR']
    if '_jsuid' in request.COOKIES: clicky_cookie = request.COOKIES['_jsuid']
    if 'intercom-id' in request.COOKIES: intercom_id = request.COOKIES['intercom-id']
    if clicky_cookie: models.OtherDownloads.objects.create(type='it adult coloring book', ip_address=client_address,
                                                           clicky_cookie=clicky_cookie, intercom_id=intercom_id)
    return HttpResponseRedirect(link)
  else:
    return render(request, 'sections/it-coloring-book.html', {})


def vulndb(request):
  if request.method == 'POST':
    form = forms.OtherDownloadsForm(request.POST)

    if form.is_valid():
      client_address = clicky_cookie = intercom_id = ''
      fc = form.save(commit=False)
      if 'REMOTE_ADDR' in request.META: client_address = request.META['REMOTE_ADDR']
      if '_jsuid' in request.COOKIES: clicky_cookie = request.COOKIES['_jsuid']
      if 'intercom-id' in request.COOKIES: intercom_id = request.COOKIES['intercom-id']

      fc.ip_address = client_address
      fc.clicky_cookie = clicky_cookie
      fc.intercom_id = intercom_id
      fc.type = 'vulndb'
      fc.name = form.cleaned_data['name']
      fc.email = form.cleaned_data['email']
      fc.ip_address = client_address
      fc.save()

      request.session['temp_data'] = form.cleaned_data
      return thanks(request, id='7')
    else:
      return render(request, 'sections/vulndb.html', {'form': form})
  else:
    form = forms.OtherDownloadsForm()

  return render(request, 'sections/vulndb.html', {'form': form})


@never_cache
def vulnerability_management_software(request):
  if request.method == 'POST':
    form = forms.OtherDownloadsForm(request.POST)

    if form.is_valid():
      fc = form.save(commit=False)
      client_address = clicky_cookie = intercom_id = ''
      if 'REMOTE_ADDR' in request.META: client_address = request.META['REMOTE_ADDR']
      if '_jsuid' in request.COOKIES: clicky_cookie = request.COOKIES['_jsuid']
      if 'intercom-id' in request.COOKIES: intercom_id = request.COOKIES['intercom-id']
      fc.clicky_cookie = clicky_cookie
      fc.intercom_id = intercom_id
      fc.name = form.cleaned_data['name']
      fc.email = form.cleaned_data['email']
      fc.ip_address = client_address
      fc.type = 'vulndb'
      form.save()

      request.session['temp_data'] = form.cleaned_data
      return redirect(resolve_url('/thanks/7/'))
  else:
    form = forms.OtherDownloadsForm()
  return render(request, 'sections/features/vulnerability-management-software.html', {'form': form})

@never_cache
@require_POST
def ajax_post(request):
  '''
  AJAX Handler for: Contact, ScheduleDemo, and Download forms
  Indicated by the POST request var 'action'
  '''
  action = request.POST.get('action', None)

  STATUS = "ko"
  response_data = {}
  from_address = 'support@device42.com'

  if request.is_ajax() and action == 'schedule':
    try:
      recipients = ['scanelli@device42.com', 'al.rossini@device42.com', ]
      recipients_alt = ['raj@rajlog.com', ]
      recipients_DEV = ['dave.amato@device42.com', ]
      main = request.POST.get('main')

      if main == '':
        form = forms.ScheduleForm(request.POST)
        if form.is_valid():
          fc = form.save(commit=False)

          the_cookie = request.META.get('hubspotutk', None)
          fc.ip_address = client_address = request.META.get('REMOTE_ADDR', '')
          fc.clicky_cookie = request.META.get('_jsuid', '')
          fc.intercom_id = request.META.get('intercom-id', '')
          the_ref = request.META.get('HTTP_REFERER', None)

          fc.name = name = form.cleaned_data['name']
          fc.email = sender = form.cleaned_data['email']
          fc.phone = phone = form.cleaned_data['phone']

          fc.save()

          subject = "FYI: Online Demo - %s - already sent an invite " % sender

          message2 = '''

    	Name: %s
    	Sender: %s
    	Phone: %s
    	IP: %s

    	''' % (name, sender, phone, client_address)

          if settings.DEBUG:
            recipients = recipients_DEV
            recipients_alt = recipients_DEV

          send_mail(subject, message2, from_address, recipients)

          if not settings.DEBUG:
            view_logic.immediate_schedule_demo_send(name, sender)
            view_logic.hubspot_data_send('schedule_demo', the_cookie, client_address, the_ref, name, sender, None, None,
                                         None, phone)

          request.session['temp_data'] = form.cleaned_data
          response_data['status'] = 'ok'
      else:
        response_data['status'] = 'ko'
        response_data['error'] = 'main was not empty'
        send_to = recipients_alt

        if settings.DEBUG:
          send_to = recipients_DEV

        send_mail('demo -ve', str(request.POST), from_address, send_to)
    except:
      pass
  elif request.is_ajax() and action == 'trial':
    try:
      main = request.POST.get('main')
      form = forms.DownloadForm(request.POST)
      if main == '' and form.is_valid():
        fc = form.save(commit=False)

        the_cookie = request.META.get('hubspotutk', None)
        client_address = fc.ip_address = request.META.get('REMOTE_ADDR', '')
        clicky_cookie = fc.clicky_cookie = request.META.get('_jsuid', '')
        intercom_id = fc.intercom_id = request.META.get('intercom-id', '')
        the_ref = request.META.get('HTTP_REFERER', None)
        name = fc.name = form.cleaned_data['name']
        email = fc.email = form.cleaned_data['email']

        if view_logic.get_validate(email) == False:
          response_data['error_msg'] = _("Please use a valid work email address")
          response_data['error'] = 'not-valid-email'
          response_data['status'] = 'ko'
        elif name == '' or email == '':
          response_data['error_msg'] = _("Please fill out all required fields")
          response_data['status'] = 'ko'
          response_data['error'] = 'required field'
        else:
          response_data['status'] = 'ok'
          download_uuid = str(uuid.uuid1())
          dwnld = models.DownloadModel(name=name, email=email, ip_address=client_address, download_uuid=download_uuid,
                                       clicky_cookie=clicky_cookie, intercom_id=intercom_id)
          subject = 'Download'
          message2 = '''
  Download Form
  Name: %s
  Sender: %s
  Client IP: %s
          ''' % (name, email, client_address)
          fc.save()
          from_address = 'support@device42.com'
          recipients = ['raj@rajlog.com']
          if settings.DEBUG:
            recipients = ['dave.amato@device42.com']
          else:
            view_logic.hubspot_data_send('download', the_cookie, client_address, the_ref, name, email)

          view_logic.immediate_download_send(request, name, email, download_uuid)
    except:
      response_data['status'] = 'ko'
      response_data['error'] = 'could not process'
      response_data['error_msg'] = _("There was an error while processing your request.   Please try again later.")
      pass
  elif request.is_ajax() and action == 'contact':
    try:
      main = request.POST.get('main')
      form = forms.ContactForm(request.POST)
      if main == '' and form.is_valid():
        fc = form.save(commit=False)

        the_cookie = request.META.get('hubspotutk', None)
        client_address = fc.ip_address = request.META.get('REMOTE_ADDR', '')
        clicky_cookie = fc.clicky_cookie = request.META.get('_jsuid', '')
        intercom_id = fc.intercom_id = request.META.get('intercom-id', '')
        the_ref = request.META.get('HTTP_REFERER', None)
        name = fc.name = form.cleaned_data['name']
        email = fc.email = form.cleaned_data['email']
        phone = fc.phone = form.cleaned_data['phone']
        topic = fc.topic = form.cleaned_data['topic']
        message = fc.message = form.cleaned_data['message']

        if view_logic.get_validate(email) == False:
          response_data['error_msg'] = _("Please use a valid work email address")
          response_data['error'] = 'not-valid-email'
          response_data['status'] = 'ko'
        else:
          if topic == '':
            topic = 'General'

          message2 = '''

            Name: %s
            Sender: %s
            Phone: %s
            Topic: %s
            Message: %s
            IP: %s

          ''' % (name, email, phone, topic, message, client_address)

          recipients = ['raj@rajlog.com', 'scanelli@device42.com', ]
          recipients_alt = ['raj@rajlog.com', ]
          recipients_DEV = ['dave.amato@device42.com', ]

          if settings.DEBUG:
            recipients = recipients_DEV
            recipients_alt = recipients_DEV
          else:
            fc.save()
            view_logic.hubspot_data_send('contact', the_cookie, client_address, the_ref, name, email, topic, message,
                                         phone)
          response_data['status'] = 'ok'

          send_mail('Contact Page [%s]' % topic, message2, from_address, recipients)
      else:
        response_data['status'] = 'ko'
        response_data['error'] = 'form not valid'
        if name == '' or email == '' or topic == '':
          response_data['error'] = 'required field'

        if settings.DEBUG:
          recipients_alt = recipients_DEV
        send_mail('contact -ve', message2, from_address, recipients_alt)
    except Exception, e:
      response_data['status'] = 'ko'
      response_data['error'] = 'error processing email'
      response_data['server_error'] = e
      print e
      pass
  return JsonResponse(response_data)


def _getMigrations():
  MIGRATIONS = {
    'Aperture VISTA': 'aperture',
    'SolarWinds IPAM': 'solarwinds-ipam',
    'OpenDCIM': 'opendcim',
    'RackTables': 'racktables',
    'RackMonkey': 'rackmonkey',
    'phpIPAM': 'phpipam',
  }
  return MIGRATIONS


def _getIntegrationDetails():
  INTEGRATION_LOGOS = "img/customers/integrations/%s.png"

  return ({
            "title": "JIRA",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'jira'),
            "description": _(
              "This connector syncs data between the Device42 CMDB and JIRA or JIRA Service Desk.  From within JIRA, users can directly select Device42 Configuration Items(CIs) when creating a JIRA issue or service request."),
            "link": resolve_url(integrations_detail, 'jira')
          },
          {
            "title": "Microsoft SCCM",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'sccm'),
            "description": _(
              "Already have Microsoft Systems Center Configuration Manager (SCCM) set up and populated with an inventory of all or a majority of your systems? Avoid duplicate auto-discovery, and take advantage of the D42-SCCM Integration to pull existing data and CIs directly into Device42."),
            "link": resolve_url(integrations_detail, 'sccm')
          },
          {
            "title": "ServiceNow",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'servicenow'),
            "description": _(
              "Using the Device42 - ServiceNow integration connector, ServiceNow users can synchronize Device42's enhanced asset management and tracking capabilities to their ServiceNow configuration items (CI) data maintained inside ServiceNow's Configuration Management Database (CMDB)."),
            "link": resolve_url(integrations_detail, 'service-now')
          },
          {
            "title": "ServiceNow Express",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'servicenow-express'),
            "description": _("Using the Device42 - ServiceNow Express Sync Script integration, ServiceNow Express users can synchronize Device42's enhanced asset management and tracking capabilities to their ServiceNow Express instance."),
            "link": resolve_url(integrations_detail, 'servicenow-express')
          },
          {
            "title": "Rundeck",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'rundeck'),
            "description": _(
              "This integration allows for Rundeck automation to be orchestrated using up-to-date Device42 CMDB information."),
            "link": resolve_url(integrations_detail, 'rundeck')
          },
          {
            "title": "Confluence",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'confluence'),
            "description": _(
              "This connector makes the devices in Device42 to be added to Confluence articles. Users can choose links/details or tables from Device42 from within their Confluence articles."),
            "link": resolve_url(integrations_detail, 'confluence')
          },
          {
            "title": "BMC Remedy",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'bmc'),
            "description": _(
              "If you are using BMC Remedy for your ITSM or even as a part of your ITIL framework- one of the biggest challenges is keeping the configuration item info up-to-date."),
            "link": resolve_url(integrations_detail, 'bmc-remedy')
          },
          {
            "title": "Zendesk",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'zendesk'),
            "description": _(
              "Easily add this free module to your Zendesk installation via the Zendesk Marketplace, and begin including accurate Device42 CI in your Zendesk tickets today!"),
            "link": resolve_url(integrations_detail, 'zendesk')
          },
          {
            "title": "StackStorm",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'stackstorm'),
            "description": _(
              "StackStorm is a powerful if-this-then-that type tool that helps you automate your workflows and changes to your infrastructure based on predefined 'trigger' criteria taking place anywhere across your environment."),
            "link": resolve_url(integrations_detail, 'stackstorm')
          },
          {
            "title": "Zapier",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'zapier'),
            "description": _(
              "Zapier is a powerful workflow automation with a simple if-this-then-that user interface.  It makes workflow automation easier by enabling changes to be made to your infrastructure based on predefined 'triggers' that can occur anywhere across your environment."),
            "link": resolve_url(integrations_detail, 'zapier')
          },
          {
            "title": "Infoblox",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'infoblox'),
            "description": _("Enhance your IPAM with the InfoBlox / Device42 integration.  Easily utilize this free script to gather information from an Infoblox installation and send it to your Device42 appliance via the REST APIs."),
            "link": resolve_url(integrations_detail, 'infoblox')
          },
          {
            "title": "Ansible",
            "image": staticfiles_storage.url(INTEGRATION_LOGOS % 'ansible'),
            "description": _("With Device42 integration, Ansible has near real-time access to your infrastructure's inventory, making it an even more capable automation solution."),
            "link": resolve_url(integrations_detail, 'ansible')
          }
  )


def _getVideos():
  VIDEOS = ({
              "slug": "dcim-demo",
              "title": _("Device42 DCIM Quick Demo"),
              "image": staticfiles_storage.url("img/sections/support/videos/Device42-DCIM-demo.png"),
              "description": _("Watch a Quick Device42 DCIM functionality demo. Duration ~ 12 minutes."),
              "video_id": "4wf363hrwr",
            },
            {
              "slug": "hierarchy",
              "title": _("Hierarchy"),
              "image": staticfiles_storage.url("img/sections/support/videos/hierarchy.png"),
              "description": _("Gain a basic understanding of Device42's hierarchy and terminology."),
              "video_id": "5ic4mi3xmq",
            },
            {
              "slug": "basic-navigation",
              "title": _("Basic Navigation"),
              "image": staticfiles_storage.url("img/sections/support/videos/basic-navigation.png"),
              "description": _(
                "Basic navigation explains the simple and consistent user interface in Device42. The video introduces Device42's navigation, including list views, search, filter, and bulk actions. See how easy it is to manage your IT Infrastructure."),
              "video_id": "vzjs61pdgj",
            },
            {
              "slug": "server-rooms",
              "title": _("Server Rooms"),
              "image": staticfiles_storage.url("img/sections/support/videos/server-rooms.png"),
              "description": _(
                "An overview of rooms in Device42, including room details, room layout view, and features like drag and drop."),
              "video_id": "s1a7jglham",
            },
            {
              "slug": "managing-racks",
              "title": _("Rack Management"),
              "image": staticfiles_storage.url("img/sections/support/videos/managing-racks.png"),
              "description": _("Web based rack layouts with drag and drop support."),
              "video_id": "hwni7jvebp"
            },
            {
              "slug": "patch-panel-management",
              "title": _("Patch Panel Management"),
              "image": staticfiles_storage.url("img/sections/support/videos/patch-panel-management.png"),
              "description": _("Cable Management with web based interface."),
              "video_id": "q29whe46w5",
            },
            {
              "slug": "ip-address-management",
              "title": _("IP Address Management"),
              "image": staticfiles_storage.url("img/sections/support/videos/switch_impact_chart.png"),
              "description": _(
                "IP Address Management(IPAM) with IPv4/IPv6 and overlapping IP ranges support with Device42."),
              "video_id": "t73hcu61mj",
            },
            {
              "slug": "enterprise-password-management",
              "title": _("Enterprise Password Management"),
              "image": staticfiles_storage.url("img/sections/support/videos/enterprise-password-management.png"),
              "description": _("Manage network passwords securely with granular permission control."),
              "video_id": "uul9xu341e",
            },
            {
              "slug": "autodiscovery",
              "title": _("Device42 Auto-discovery Introduction"),
              "image": staticfiles_storage.url("img/sections/support/videos/Device42-auto-discovery-process.png"),
              "description": _(
                "This video Introduces Device42 IT infrastructure management software's auto-discovery functionality. In this video we will discuss the process of auto-discovery, the best practices for running the initial Device42 auto-discovery, and demonstrate how discoveries build a comprehensive, accurate asset database in Device42 DCIM software. We'll also address a few frequently asked questions and provide links to additional auto-discovery resources."),
              "video_id": "qr7ght1mcz",
            })
  return VIDEOS
def _getUtilities():
  UTILITIES = {
    _('Auto Discovery'): 'autodiscovery',
    _('Update'): 'update',
    _('Bulk Data Management'): 'bulk-data-management',
    # _('Device42 Download'): 'device42-download',
    _('Miscellaneous Tools'): 'miscellaneous-tools',
  }
  return UTILITIES
def _getIntegrations():
  return {
    'JIRA': 'jira',
    'Confluence': 'confluence',
    'ServiceNow': 'service-now',
    'ServiceNow Express': 'servicenow-express',
    'Rundeck': 'rundeck',
    'Zendesk': 'zendesk',
    'Microsoft SCCM': 'sccm',
    'BMC Remedy': 'bmc-remedy',
    'StackStorm': 'stackstorm',
    'Zapier': 'zapier',
    'Infoblox': 'infoblox',
    'Ansible': 'ansible',
  }
def _getClientLogos():
  LOGOS = CLIENT_LOGOS = {
    "ucsb": "ucsb.png",
    "fijitsu": "fijitsu.png",
    "appdynamics": "appdynamics.png",
    "mercedesbenz": "mercedesbenz.png",
    "westerndigital": "westerndigital.png",
    "qlik": "qlik.png",
    "jasper": "jasper.png",
    "bt": "bt.png",
    "jll": "jll.png",
    "singtel": "singtel.png",
    "apptio": "apptio.png",
    "homeaway": "homeaway.png",
    "mitre": "mitre.png",
    "livingsocial": "livingsocial.png",
    "concur": "concur.png",
    "fifgroup": "fifgroup.png",
    "bottomline": "bottomline.png",
    "optus": "optus.png",
    "pico": "pico.png",
    "peak6": "peak6.png",
    "atlassian": "atlassian.png",
    "sprint": "sprint.png",
    "verizon": "verizon.png",
    "stackoverflow": "stackoverflow.png",
    "schoolofbeijing": "schoolofbeijing.png",
    "avaya": "avaya.png"
  };
  return LOGOS
def _getJobs():
  return {
    0: _("DevOps Evangelist"),
  }


class AjaxDownloadFill(View):
  def post(self, request):
    the_matrix = {'name': '',
                  'email': '',
                  'vp': '',
                  'eula': 'on',
                  'name_error': False,
                  'email_error': False,
                  'platform_error': False,
                  'eula_error': False,
                  'errors': False,
                  }
    if 'main' in request.POST and 'email' in request.POST and 'name' in request.POST and 'csrftoken' in request.POST and \
        request.POST['main'] == '':
      if 'CSRF_COOKIE' in request.META and request.META['CSRF_COOKIE'] == request.POST['csrftoken']:
        the_email = request.POST['email']
        the_validation = True
        if '@' not in the_email:
          the_validation = False
          the_matrix['email_error'] = True
          return Response(500, content={'code': 0, 'msg': the_matrix, 'validation': the_validation})
        domain_lower = the_email.split('@')[1].lower()
        if (domain_lower in INCOGNITO_LIST) or ('yahoo.' in domain_lower):
          the_validation = False
          the_matrix['email_error'] = True
          client_address = title = clicky_cookie = intercom_id = ''
          if 'REMOTE_ADDR' in request.META:
            client_address = request.META['REMOTE_ADDR']
          if 'title' in request.POST:
            title = request.POST['title']
          if '_jsuid' in request.COOKIES:
            clicky_cookie = request.COOKIES['_jsuid']
          the_type = 'download'
          if 'type' in request.POST and request.POST['type'] == 'demo':
            the_type = 'demo'
          IncognitoDownloads.objects.create(name=request.POST['name'],
                                            email=the_email,
                                            ip_address=client_address,
                                            clicky_cookie=clicky_cookie,
                                            tipe=the_type,
                                            title=title,
                                            post_data=request.POST,
                                            meta_data=request.META)
          return Response(500, content={'code': 0, 'msg': the_matrix, 'validation': the_validation})
        else:
          the_matrix, the_validation = view_logic.validate_download_form(the_matrix, request.POST)
          if the_validation:
            client_address = title = clicky_cookie = intercom_id = ''
            if 'hubspotutk' in request.COOKIES:
              the_cookie = request.COOKIES['hubspotutk']
            else:
              the_cookie = None
            if 'HTTP_REFERER' in request.META:
              the_ref = request.META['HTTP_REFERER']
            else:
              the_ref = None
            if 'REMOTE_ADDR' in request.META:
              client_address = request.META['REMOTE_ADDR']
            if 'title' in request.POST:
              title = request.POST['title']
            if '_jsuid' in request.COOKIES:
              clicky_cookie = request.COOKIES['_jsuid']
            if 'intercom-id' in request.COOKIES:
              intercom_id = request.COOKIES['intercom-id']
            the_type = 'download'
            if 'type' in request.POST and request.POST['type'] == 'demo':
              the_type = 'demo'
            if the_type == 'download':
              download_uuid = str(uuid.uuid1())
              dwnld = DownloadModel.objects.create(name=the_matrix['name'],
                                                   email=the_matrix['email'],
                                                   I_agree_to_EULA=True,
                                                   ip_address=client_address,
                                                   download_uuid=download_uuid,
                                                   clicky_cookie=clicky_cookie,
                                                   intercom_id=intercom_id)
              subject = 'Download'
              message2 = """
Download Form

Name: %s
Sender: %s
Client IP: %s
""" % (the_matrix['name'], the_matrix['email'], client_address)
              from_address = 'support@device42.com'
              recipients = ['raj@rajlog.com',]
              if settings.DEBUG:
                recipients = ['dave.amato@device42.com',]
              view_logic.immediate_download_send(request, the_matrix['name'], the_matrix['email'], download_uuid)
              view_logic.hubspot_data_send(title, the_cookie, client_address, the_ref, the_matrix['name'],
                                the_matrix['email'], the_matrix['vp'])

            else:
              ScheduleModel.objects.create(name=the_matrix['name'],
                                           email=the_matrix['email'],
                                           ip_address=client_address,
                                           clicky_cookie=clicky_cookie,
                                           intercom_id=intercom_id)
              message2 = """
Download Form

Name: %s
Sender: %s
Client IP: %s
""" % (the_matrix['name'], the_matrix['email'], client_address)
              from_address = 'support@device42.com'
              recipients = ['scanelli@device42.com', 'al.rossini@device42.com', ]  # 'raj@rajlog.com',
              if settings.DEBUG:
                recipients = ['dave.amato@device42.com',]
              subject = "FYI: online demo - already sent an invite "

              send_mail(subject, message2, from_address, recipients)
              view_logic.immediate_schedule_demo_send(the_matrix['name'], the_matrix['email'])
              view_logic.hubspot_data_send(title, the_cookie, client_address, the_ref, the_matrix['name'],
                                the_matrix['email'], the_matrix['vp'], None, None, None, 'demo')
          else:
            # print 'download form filled - errors', request.POST, request.META
            return Response(500, content={'code': 0, 'msg': the_matrix, 'validation': the_validation})
      else:
        recipients = ['raj@rajlog.com',]
        if settings.DEBUG:
          recipients = ['dave.amato@device42.com']
        send_mail('download -ve', str(request.POST), 'support@device42.com', recipients)
    else:
      recipients = ['raj@rajlog.com',]
      if settings.DEBUG:
        recipients = ['dave.amato@device42.com',]
      send_mail('download -ve', str(request.POST), 'support@device42.com', recipients)
    request.session['temp_data'] = the_matrix
    return Response(200, content={'code': 0, 'msg': 'done'})

class HubSpotFormFill(View):
  permissions = (AllowAny,)

  def post(self, request):
    print request, self
    return Response(200, content={'done'})

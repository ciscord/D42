import os, sys, requests, traceback, user_agents, time, base64, hmac, urllib, hashlib, json
from datetime import datetime, timedelta
from IPy import IP
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext as _
import project
from project.apps.device42.models import GeoIPDB, OtherDownloads, CurrentCustomers
from project.apps.device42 import incognitos


def encode(aws_secret_access_key, str, urlencode=False):
  b64_hmac = base64.encodestring(hmac.new(aws_secret_access_key, str, hashlib.sha1).digest()).strip()
  if urlencode:
    return urllib.quote_plus(b64_hmac)
  else:
    return b64_hmac


def query_args_hash_to_string(query_args):
  pairs = []
  for k, v in query_args.items():
    piece = k
    if v is not None:
      piece += "=%s" % urllib.quote_plus(str(v))
    pairs.append(piece)

  return '&'.join(pairs)


def generate_download_links(expires):
  import boto
  key_pair_id = "APKAJ3OPRB6IA4TA23CA"
  priv_key_filename = "pk-APKAJ3OPRB6IA4TA23CA.pem"
  priv_key_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))), 'credentials', priv_key_filename)

  cf = boto.connect_cloudfront()
  dist = cf.get_distribution_info('E111F17TJ5VJRY')

  link_names = [
    {'name': 'VMware ESX/ESXi ', 'link': 'https://d17xs64pqeg3rv.cloudfront.net/Device42-64-11.6.1-ovf.7z',
     'size': '1.8 GB',
     'img_src': 'http://d42i.s3.amazonaws.com/media/images/links/vmware.png'},
    {'name': 'Oracle Virtual Box/VMware Player',
     'link': 'https://d17xs64pqeg3rv.cloudfront.net/Device42-64-11.6.1-vmdk.7z',
     'size': '1.4 GB',
     'img_src': "http://d42i.s3.amazonaws.com/media/images/links/virtual_box.png"},
    {'name': 'Citrix Xenserver', 'link': 'https://d17xs64pqeg3rv.cloudfront.net/Device42-64-11.6.1-xva.7z',
     'size': '1.0 GB',
     'img_src': "http://d42i.s3.amazonaws.com/media/images/links/citrix_xen.png"},
    {'name': 'Microsoft HyperV', 'link': 'https://d17xs64pqeg3rv.cloudfront.net/Device42-64-11.6.1-vhd.7z',
     'size': '1.3 GB',
     'img_src': "http://d42i.s3.amazonaws.com/media/images/links/hyperv.png"},
    {'name': 'Xen/KVM Raw image', 'link': 'https://d17xs64pqeg3rv.cloudfront.net/Device42-64-11.6.1-raw.zip',
     'size': '2.0 GB',
     'img_src': "http://d42i.s3.amazonaws.com/media/images/links/kvm_qemu_raw.png"},
  ]

  download_links = []
  for _dict in link_names:
    http_signed_url = dist.create_signed_url(_dict['link'], key_pair_id, expires, private_key_file=priv_key_file)
    download_links.append(
      {'name': _dict['name'], 'link': http_signed_url, 'size': _dict['size'], 'img_src': _dict['img_src']})
  return download_links


def validate_download_form(the_matrix, args):
  the_matrix['name'] = args['name']
  the_matrix['email'] = args['email']

  if args['name'] != '' and args['email'] != '':
    if get_validate(args['email']):
      return the_matrix, True
    else:
      the_matrix['email_error'] = True
      return the_matrix, False
  else:
    if args['name'] == '':
      the_matrix['name_error'] = True
    if args['email'] == '':
      the_matrix['email_error'] = True
    return the_matrix, False


def generate_link_generic(path, storage_bucket='d42-auto-discover'):
  expires = int(time.time() + 172800)
  query_args = {}
  canonical_str = str(expires)
  storage_url = 'https://s3.amazonaws.com'

  if 'OpenDisc' in path: storage_bucket = 'd42-open-discover'
  # string_to_sign = "GET\n\n\n" + canonical_str + "\n" + "/d42-auto-discover/%s" % path
  string_to_sign = "GET\n\n\n" + canonical_str + "\n" + "/%s/%s" % (storage_bucket, path)
  # url = 'https://s3.amazonaws.com/d42-auto-discover/%s' % path
  url = '%s/%s/%s' % (storage_url, storage_bucket, path)
  encoded_canonical = encode('kOvhzMuq/yuXdxyjhYa7dk6XfXWsI1Q+JaQ0Lkm9', string_to_sign)
  # url += "/%s" % urllib.quote_plus('kOvhzMuq/yuXdxyjhYa7dk6XfXWsI1Q+JaQ0Lkm9')
  query_args['Signature'] = encoded_canonical
  query_args['Expires'] = expires
  query_args['AWSAccessKeyId'] = 'AKIAIS2U7NVNTQXL7AMQ'
  url += "?%s&FixForIE=.exe" % query_args_hash_to_string(query_args)
  return url


def generate_link_software(package, request, form=None):
  from django.core.urlresolvers import reverse, resolve
  download = request.POST.get('download')
  if package in project.views._getUtilities().values():
    url = client_address = clicky_cookie = intercom_id = ''
    the_cookie = the_ref = None
    update_type = 'regular'

    try:
      client_address = request.META['HTTP_X_FORWARDED_FOR']
    except:
      client_address = request.META['REMOTE_ADDR']

    if 'HTTP_REFERER' in request.META: the_ref = request.META['HTTP_REFERER']
    if '_jsuid' in request.COOKIES: clicky_cookie = request.COOKIES['_jsuid']
    if 'hubspotutk' in request.COOKIES: the_cookie = request.COOKIES['hubspotutk']
    if 'intercom-id' in request.COOKIES: intercom_id = request.COOKIES['intercom-id']
    if package != "update": OtherDownloads.objects.create(type=('%s' % download), ip_address=client_address,
                                                    clicky_cookie=clicky_cookie, intercom_id=intercom_id)
    if form is not None:
      fc = form.save(commit=False)

    if package == "opendiscovery":
      if download == "open disc msi":
        url = generate_link_generic('D42OpenDiscv202.msi')
      if download == "open disc bin":
        url = generate_link_generic('D42OpenDiscv202.zip')
    elif package == "autodiscovery":
      if download == ".net auto disc tool":
        url = generate_link_generic('D42AutoDisc_v1150.exe')
      elif download == "linux auto disc tool":
        url = generate_link_generic('d42_linuxautodisc_v1.3.3.zip')
      elif download == ".net ping sweep":
        url = generate_link_generic('d42_pingsweep_v3.1.0.zip')
      elif download == "netflow":
        url = generate_link_generic('d42-netflow-collector-v100.zip')
    elif package == "miscellaneous-tools":
      if download == "d42 print utility":
        url = generate_link_generic('D42PrintInstaller_v1.0.1.BETA.msi')
    elif package == "bulk-data-management":
      if download == "generic import tool":
        url = generate_link_generic('d42_generic_import_tool_v7.2.4.exe')
    elif package == "update":
      if download == "update-regular" or download == "update-pma":
        if download == "update-pma":
          update_type = 'pma'

        if form is not None:
          fc.update_type = update_type
          fc.ip_address = client_address
          fc.save()

        subject = 'update'
        sender = form.cleaned_data['email']
        message2 = 'Update Form: Sender: %s Client IP: %s' % (sender, client_address)
        from_address = 'support@device42.com'
        recipients = ['scanelli@device42.com']
        if settings.DEBUG:
          recipients = ['dave.amato@device42.com']
        immediate_update_send(sender, message2, update_type)
        hubspot_data_send('update',the_cookie,client_address,the_ref,'',sender, None, message2)
        if form is not None:  request.session['temp_data'] = form.cleaned_data
        return '/thanks/2/' #reverse('project.views.thanks', kwargs={'id': '2'})

    if form is not None:  request.session['temp_data'] = form.cleaned_data

  else:
    return resolve(request.path_info).url_name

  return url


def immediate_update_send(sender, message, update_type):  # , curver name
  recipients = ['raj@rajlog.com', 'scanelli@device42.com', ]
  if settings.DEBUG: recipients = ['dave.amato@device42.com']
  the_domain = sender.split('@')[1]
  if (CurrentCustomers.objects.filter(email_domain=the_domain) and the_domain.split('.')[0] not in ['gmail', 'yahoo',
                                                                                                    'hotmail', 'me',
                                                                                                    'mail',
                                                                                                    'outlook']) or the_domain == 'device42.com':
    text_content, html_content = text_html_calculate_updatelink(update_type)
    if update_type == 'pma':
      subject = _('Device42 Power Monitoring Appliance Update')
    else:
      subject = _('Device42 Update')
    send_mailgun_message("Device42 Support Team <support@corp.device42.com>", sender, subject, text_content,
                         html_content)
    send_mail('update', message, 'support@device42.com', recipients)
  else:
    send_mail('update not emailed', message, 'support@device42.com', recipients)


def text_html_calculate_updatelink(update_type):
  if update_type == 'pma':
    link = generate_link_generic('update-4.0.4.1482420556.zip.enc', 'device42')
    release_notes = 'http://blog.device42.com/tag/power-appliance/'
  else:
    link = generate_link_generic('update-1010-to-11.7.0.1483732141.zip.enc', 'device42')
    release_notes = 'http://blog.device42.com/tag/release/'

  textmessage = _("""
  Hi,

  Please click below to download the Device42 update you recently requested. This link is valid for the 72 hours.

  Download update:  %s


  Instruction on how to upgrade can be found at:  https://device42.zendesk.com/entries/21783332

  Read about the latest release here:  %s

  Please reply to this email if you have issues applying the update.

  Regards,
  Device42 Support Team.
  """) % (link, release_notes)

  htmlmessage = _("""
  <html><head></head><body>
  Hi,
  <p>Please <a href='%s'>click here</a> to download the Device42 update you recently requested.   This link is valid for the next 72 hours.</p>
  <p>For instructions on how to apply the update, <a href="https://device42.zendesk.com/entries/21783332">go here</a>.</p>
  <p>Read about the latest release notes <a href="%s">here</a>.</p>

  <p>Please reply to this email if you have issues applying the update. </p>

  Regards,<br>Device42 Support Team.
  </body></html>""") % (link, release_notes)

  return textmessage, htmlmessage


def send_mailgun_message(from_email, to_email, the_subject, text, html, bcc=None):  # ,
  if to_email.split('@')[1] in ['mail.ru', 'mailinator.com', ]: return -1 #todo out - take care in incognito check
  try:
    mail_post = requests.post(
      "https://api.mailgun.net/v2/corp.device42.com/messages",
      auth=("api", "key-08k09z9jf7jyte7vi22nozc-bgk7g-s2"),
      data={"from": from_email,
            "to": to_email,
            "subject": the_subject,
            "text": text,
            "html": html,
            "v:my-custom-data": the_subject,
            "bcc": bcc
            })
    if mail_post.status_code != requests.codes.ok:
      print mail_post, mail_post.json()
      error_sending_msg(to_email, the_subject, text, html, from_email)
  except Exception as e:
    print 'error sending message', the_subject, to_email, str(e)
    error_sending_msg(to_email, the_subject, text, html, from_email)


def error_sending_msg(to_email, the_subject, text, html, from_email='support@device42.com'):
  from django.core.mail import EmailMessage, EmailMultiAlternatives
  receiveremail = ['raj@rajlog.com', ]
  if settings.DEBUG:
    receiveremail = ['dave.amato@device42.com', ]
  msg = EmailMessage('Device42 Message Send Error (via mailgun)', the_subject + ' ' + to_email, from_email,
                     receiveremail)
  msg.send()
  msg2 = EmailMultiAlternatives(the_subject, text, from_email, [to_email])
  msg2.attach_alternative(html, "text/html")
  msg2.send()


def hubspot_data_send(the_method, the_cookie, client_address, the_ref, name, email, topic=None, message=None,
                      phone=None, company=None, type=None):
  try:
    if ' ' in name:
      firstname = name.split(' ')[0]
      lastname = name.split(' ', 1)[1]
    else:
      firstname = name
      lastname = ''
    the_data = {"firstname": firstname,
                "lastname": lastname,
                "email": email,
                "hs_context": json.dumps({
                  "ipAddress": client_address,
                  "hutk": the_cookie,
                  "pageUrl": the_ref,
                  "pageName": the_method
                })
                }
    if the_method == 'download':
      form_id = '590b7b91-57e2-4ffc-9acb-6b9a1c81731c/'
    elif the_method == 'update':
      form_id = '271cc1bd-1ca4-4e23-a764-8d209f79eefb/'
    elif the_method == 'contact':
      form_id = '45503623-2e8c-4368-b9ff-d0ce2501a568/'
      the_data.update({'phone': phone, 'topic': topic, 'message': message})
    elif the_method == 'schedule_demo' or type == 'demo':
      form_id = '991eed0a-179a-4091-808a-72b35453108a/'
      if phone: the_data.update({'phone': phone})
    else:
      form_id = '590b7b91-57e2-4ffc-9acb-6b9a1c81731c/'
    the_url = "https://forms.hubspot.com/uploads/form/v2/433338/" + form_id
    hub_post = requests.post(
      the_url,
      # auth=("api", "key-08k09z9jf7jyte7vi22nozc-bgk7g-s2"),
      data=the_data)
    if hub_post.status_code == 204:
      pass
    else:
      print 'failed hubspot', hub_post
      # error_sending_msg(from_email, to_email, the_subject, text, html)
  except Exception as e:
    print 'error sending hubspot data', name, email, str(e)


def get_validate(email):
  try:
    _email = email.split('@')[1]
    if _email not in incognitos.INCOGNITO_LIST:
      return False
    else:
      return True
    # mg_result = requests.get(
    #   "https://api.mailgun.net/v2/address/validate",
    #   auth=("api", "pubkey-8gjl8zluch9vjktwusqpfzjz438jil20"),
    #   params={"address": email}).json()
    # return mg_result["is_valid"]
  except:
    import re
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
      return False
    else:
      return True


def send_email(subject, message, sender, to_list):
  if subject and message and sender:
    try:
      send_mail(subject, message, sender, to_list)
    except BadHeaderError:
      return HttpResponse('Invalid header found.')
    return HttpResponseRedirect('/thanks/9/')
  else:
    return HttpResponse(_("Make sure all fields are entered and valid."))


def parse_user_agent(ua):
  parsed_ua = user_agents.parse(ua)
  return parsed_ua.is_bot


def get_ip_data(ipaddress):
  continent = country = ''
  if IP(ipaddress).iptype() == 'PUBLIC':
    if GeoIPDB.objects.filter(ip=ipaddress):
      ipobj = GeoIPDB.objects.filter(ip=ipaddress)[0]
      if ipobj.last_updated < datetime.today() - timedelta(days=180):  # cache for 180 days?
        continent, country = store_ip_data(ipaddress)
      else:
        continent = ipobj.continent
        country = ipobj.country
    else:
      continent, country = store_ip_data(ipaddress)
  return continent, country


def store_ip_data(ipaddress):
  try:
    import geoip2.webservice
    client = geoip2.webservice.Client(109451, 'YfeYya1KZ1AH')
    response = client.city(ipaddress)
    city = country = domain = org = subdivision = timezone = continent = latitude = longitude = ''
    try:
      city = response.city.name
    except:
      pass
    try:
      country = response.country.iso_code
    except:
      pass
    try:
      domain = response.traits.domain
    except:
      pass
    try:
      org = response.traits.organization
    except:
      pass
    try:
      subdivision = response.subdivisions.most_specific.name
    except:
      pass
    try:
      timezone = response.location.timezone
    except:
      pass
    try:
      continent = response.continent.code
    except:
      pass
    try:
      latitude = response.location.latitude
    except:
      pass
    try:
      longitude = response.location.longitude
    except:
      pass
    if GeoIPDB.objects.filter(ip=ipaddress):
      ipobj = GeoIPDB.objects.filter(ip=ipaddress)[0]
    else:
      ipobj = GeoIPDB(ip=ipaddress)
    ipobj.city = city
    ipobj.country = country
    ipobj.domain = domain
    ipobj.org = org
    ipobj.subdivision = subdivision
    ipobj.timezone = timezone,
    ipobj.continent = continent
    ipobj.latitude = latitude
    ipobj.longitude = longitude
    ipobj.full_clean()
    ipobj.save()
    return ipobj.continent, ipobj.country
  except:
    traceback.print_exc(file=sys.stdout)
    return ''


def immediate_download_send(request, name, sender, download_uuid):
  text_content, html_content = text_html_calculate_linkgenerate(request, name, download_uuid)
  send_mailgun_message("Device42 Support Team <support@corp.device42.com>", sender, "Device42 download", text_content, html_content)


def immediate_schedule_demo_send(name, sender):
  text_content, html_content = text_html_calculate_scheduledemo(name)
  send_mailgun_message("Device42 Support Team <support@corp.device42.com>", sender, "Device42 Online Demo", text_content, html_content, "Raj <raj@rajlog.com>")


def text_html_calculate_scheduledemo(first_name):
  text1 = _("Hi %s,\n") % first_name
  text2 = _("""

Thank you for your interest in Device42.

To schedule an individualized demo, just click the following link and select a time slot: https://d42demo.youcanbook.me/

If you are unable to use this link, please reply to this email with a few available time slots that work for you (and please include your time zone!).

We look forward to connect with you.

Sincerely,
Device42 Team
600 Saw Mill Rd, West Haven CT 06516
1-866-343-7242
PS: This email was automatically generated, but you can still reply to talk to an actual person :)
""")

  html1 = _("<html><head></head><body>Hi %s,") % first_name
  html2 = _("""<p>Thank you for your interest in Device42. </p>
<p>To schedule an individualized demo, just click the following link and select a time slot: <a href="https://d42demo.youcanbook.me/">https://d42demo.youcanbook.me/</a></p>

<p>If you are unable to use this link, please reply to this email with a few available time slots that work for you (and please include your time zone!).
</p><p>
We look forward to connect with you.</p>
<p>
Sincerely,<br />
Device42 Team<br />
600 Saw Mill Rd, West Haven CT 06516<br />
1-866-343-7242<br />
PS: This email was automatically generated, but you can still reply to talk to an actual person :)
</p>
</body></html>
""")
  html_content = html1 + html2
  text_content = text1 + text2
  return text_content, html_content


def text_html_calculate_linkgenerate(request, first_name, download_uuid):
  # link, size = generate_link_311(ve)
  text1 = _("Hi %s,\n") % first_name
  text2 = _("""" \

Thank you for your interest in device42. We have the virtual appliance link ready for you(link valid for a week). """)
  text3 = _("'Download link: ") + 'http://www.device42.com%s/download_links/%s/' % (
    request.LANGUAGE_CODE, download_uuid)
  text5 = _(""""

For getting started documentation and login info, please visit to: http://docs.device42.com/getstarted/

You can read about the latest release here: http://blog.device42.com/tag/release/

The appliance is production ready. Please let us know if you need an extended demo license.

After the install, you can refer to the quick start guide: http://docs.device42.com/device42-beginners-guide/

Please reply to this message with any comments or suggestions. We look forward to working with you!


Regards,
Device42 Support Team.
1-866-343-7242
""")

  html1 = _("<html><head></head><body>Hi %s,") % first_name
  html2 = _("""<p>Thank you for your interest in Device42. We have the virtual appliance link
    ready for you(valid for a week).
    """)
  html3 = _('</p><p>Download <a href="http://www.device42.com/download_links/%(uuid)s/">Here</a>.</p>') % {'uuid': download_uuid}
  html4 = ''
  html7 = _("""<p>
    The virtual appliance uses 2 vCPU, 2 GB RAM &amp; 50 GB of HDD. For installation and login info, please visit: <a  href="http://docs.device42.com/getstarted/">http://docs.device42.com/getstarted/</a>
    </p>

    <p>
    You can read about the latest release <a href="http://blog.device42.com/tag/release/">here.</a></p><p>The appliance is production ready. Please let us know if you need an extended demo license.</p>
    <p>Once the install is complete, you can refer to <a href="http://docs.device42.com/device42-beginners-guide/">the quick start guide.</a></p>
    <p>Please reply to this message with any comments or suggestions. We look forward to working with you!<p>
    Regards,<br>Device42 Support Team.<br>1-866-343-7242 <br>
     </body>
    </html>
    """)
  html_content = html1 + html2 + html3 + html4 + html7
  text_content = text1 + text2 + text3 + text5
  return text_content, html_content

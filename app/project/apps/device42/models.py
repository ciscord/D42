from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


class GeoIPDB(models.Model):
  ip = models.CharField(max_length=128, unique=True)
  city = models.CharField(max_length=128, blank=True, null=True)
  country = models.CharField(max_length=128, blank=True, null=True)
  domain = models.CharField(max_length=128, blank=True, null=True)
  org = models.CharField(max_length=128, blank=True, null=True)
  subdivision = models.CharField(max_length=128, blank=True, null=True)
  timezone = models.CharField(max_length=128, blank=True, null=True)
  continent = models.CharField(max_length=128, blank=True, null=True)
  latitude = models.CharField(max_length=128, blank=True, null=True)
  longitude = models.CharField(max_length=128, blank=True, null=True)
  added = models.DateTimeField(auto_now_add=True)
  last_updated = models.DateTimeField(auto_now=True)


class PricingContactModel(models.Model):
  name = models.CharField(_('Full Name'), max_length=128)
  email = models.EmailField(_('Email Address'))
  company = models.CharField(_('Company'), max_length=128)
  phone = models.CharField(_('Phone Number'), max_length=32, null=True, blank=True)
  country = models.CharField(_('Country'), max_length=32)
  device_count = models.CharField(_('Number of IP Addresses'), max_length=32, null=True, blank=True)
  slm_addon = models.BooleanField(_('Software License Management'), default=False)
  power_monitoring_addon = models.BooleanField(_('Power & Environmental Monitoring'), default=False)
  power_control_addon = models.BooleanField(_('Power Control'), default=False)
  referred_by_reseller = models.BooleanField(_('Referred by Reseller'), default=False)
  reseller_name = models.CharField(_('Reseller Name'), max_length=64, null=True, blank=True)
  ip_address = models.CharField(null=True, blank=True, max_length=80, editable=False)
  time_linked = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  clicky_cookie = models.CharField(null=True, blank=True, max_length=128, editable=False)


class ScheduleModel(models.Model):
  name = models.CharField(name='name', max_length=100, verbose_name=_('Name'), blank=False, null=False)
  email = models.EmailField(name='email', verbose_name=_('Work Email'), blank=False, null=False)
  phone = models.CharField(name='phone', verbose_name=_('Phone Number'), max_length=32, null=True,
                           blank=True)
  # timezone = models.CharField(name='timezone', choices=([(t, t) for t in pytz.common_timezones]), max_length=128,
  #                             verbose_name=_('Timezone'), blank=True)
  ip_address = models.CharField(null=True, blank=True, max_length=80, editable=False, verbose_name=_('IP Address'))
  time_linked = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  clicky_cookie = models.CharField(null=True, blank=True, max_length=128, editable=False)
  intercom_id = models.CharField(null=True, blank=True, max_length=128, editable=False)


class ContactModel(models.Model):
  name = models.CharField(name='name', max_length=100, verbose_name=_('Name'))
  email = models.EmailField(name='email', verbose_name=_('Work Email'))
  phone = models.CharField(name='phone', verbose_name=_('Phone Number'), max_length=32, null=True,
                           blank=True)
  topic = models.CharField(name='topic', max_length=100, verbose_name=_('Subject'), blank=True, null=False,
                           choices=(
                             ('New_Feature', _('New Feature')),
                             ('Bug', _('Bug/Problem')),
                             ('Comment', _('Comment/Testomonial')),
                             ('Other', _('Other'))
                           ))
  message = models.TextField(name='message', verbose_name=_('Message'), blank=False, null=False)
  ip_address = models.CharField(null=True, blank=True, max_length=80, editable=False, name='ip_address')
  time_linked = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  clicky_cookie = models.CharField(null=True, blank=True, max_length=128, editable=False)
  intercom_id = models.CharField(null=True, blank=True, max_length=128, editable=False)


class DownloadModel(models.Model):
  name = models.CharField(name="name", max_length=64, verbose_name=_("Name"))
  email = models.EmailField(name="email", verbose_name=_("Work Email"))
  download_uuid = models.CharField(name="download_uuid", max_length=36)
  virtual_platform = models.CharField(name="virtual_platform", max_length=20, choices=(
    ('VMware vCenter', "VMware ESX or ESXi"),
    ("VMware Player", "Oracle VirtualBox / VMware Player"),
    ("HuperV", "Microsoft HyperV"),
    ("XenServer", "Citrix XenServer"),
    ("Xen/KVM Raw Image", "Xen/KVM Raw Image")
  ), verbose_name=_("Virtual Platform"))
  I_agree_to_EULA = models.BooleanField(help_text='(<a href="/eula/">%s</a>)' % _("End User License Agreement"),
                                        default=False)
  time_linked = models.DateTimeField(auto_now_add=True)
  ip_address = models.CharField(null=True, blank=True, max_length=80, editable=False)
  clicky_cookie = models.CharField(null=True, blank=True, max_length=128, editable=False)
  intercom_id = models.CharField(null=True, blank=True, max_length=128, editable=False)


class DownloadLinks(models.Model):
  name = models.CharField(name="name", max_length=64)
  link = models.CharField(name="link", max_length=300)
  size = models.CharField(name="size", max_length=10)
  img_src = models.CharField(name="img_src", max_length=300)
  downloadmodel = models.ForeignKey(DownloadModel, on_delete=models.CASCADE)


class OtherDownloads(models.Model):
  type = models.CharField(max_length=36)
  time_linked = models.DateTimeField(auto_now_add=True)
  ip_address = models.CharField(null=True, blank=True, max_length=80, editable=False)
  clicky_cookie = models.CharField(null=True, blank=True, max_length=128, editable=False)
  intercom_id = models.CharField(null=True, blank=True, max_length=128, editable=False)
  email = models.EmailField(name='email')
  name = models.CharField(name="name", max_length=64)


class VideoModel(models.Model):
  title = models.CharField(name="title", max_length=64)
  image = models.CharField(name="image", max_length=128)
  description = models.TextField(name="description")


class FreeClient(models.Model):
  email = models.EmailField(name='email')
  Subscribe = models.BooleanField(name='Subscribe',
                                  help_text=_(
                                    '(Receive our occasional newsletter with product news and industry related tips.)'),
                                  default=False)
  ip_address = models.CharField(null=True, blank=True, max_length=80, editable=False)
  time_linked = models.DateTimeField(auto_now_add=True)
  I_agree_to_EULA = models.BooleanField(name='I_agree_to_EULA', help_text='(<a href="/d42_open_disc_eula/">%s</a>)' % _(
    'End User License Agreement'), default=False)

  def clean(self):
    if self.I_agree_to_EULA is "off":
      raise ValidationError(_("Please check the checkbox saying you agree with the End User License Agreement"))


class UpdateModel(models.Model):
  email = models.EmailField()
  time_linked = models.DateTimeField(auto_now_add=True)
  ip_address = models.CharField(null=True, blank=True, max_length=80, editable=False)
  update_type = models.CharField(choices=(('regular', 'regular'), ('pma', 'pma')), max_length=24, editable=False,
                                 default='regular')


class CurrentCustomers(models.Model):
  email_domain = models.CharField(max_length=254)
  last_updated = models.DateTimeField(auto_now=True)


ve_beta = (('vmware vcenter', 'vmware ESX or ESXi'), ('vmware player', 'vmware Player/Virtual Box'),)

class BetaSignUp(models.Model):
  name = models.CharField(max_length=64)
  email = models.EmailField(help_text='(We will not sell or share your email address. Period.)')
  virtual_platform = models.CharField(max_length=20, choices=ve_beta, default='vmware vcenter', editable=False)
  I_agree_to_EULA = models.BooleanField(help_text='(<a href="/eula">End User License Agreement</a>)', editable=False)
  time_linked = models.DateTimeField(auto_now_add=True)

class IDsProcessed(models.Model):
  id_processed_download = models.PositiveIntegerField(blank=True, null=True)
  id_processed_contact = models.PositiveIntegerField(blank=True, null=True)
  id_processed_demo = models.PositiveIntegerField(blank=True, null=True)
  id_processed_update = models.PositiveIntegerField(blank=True, null=True)
  id_processed_idc = models.PositiveIntegerField(blank=True, null=True)
  id_processed_pricingcontact = models.PositiveIntegerField(blank=True, null=True)

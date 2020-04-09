from django.forms import ModelForm, TextInput, Textarea
from django.utils.translation import ugettext_lazy as _

from project.apps.device42 import models
from project.apps.device42.incognitos import INCOGNITO_LIST


class DownloadForm(ModelForm):
  class Meta:
    model = models.DownloadModel
    fields = ('name', 'email',)
    widgets = {
      'name': TextInput(attrs={'placeholder': _('Name')}),
      'email': TextInput(attrs={'placeholder': _('Email Address')}),
    }
  def clean_email(self):
    from django.core.exceptions import ValidationError
    email = self.cleaned_data['email']
    if email.split('@')[1] in INCOGNITO_LIST:
      raise ValidationError(_('Please use a valid work email address.'))
    return email

class OtherDownloadsForm(ModelForm):
  class Meta:
    model = models.OtherDownloads
    fields = ('name', 'email',)
    widgets = {
      'name': TextInput(attrs={'placeholder': _('Name')}),
      'email': TextInput(attrs={'placeholder': _('Email Address')}),
    }
  def clean_email(self):
    from django.core.exceptions import ValidationError
    email = self.cleaned_data['email']
    if email.split('@')[1] in INCOGNITO_LIST:
      raise ValidationError(_('Please use a valid work email address.'))
    return email

class ContactForm(ModelForm):
  class Meta:
    model = models.ContactModel
    fields = ('name', 'email', 'phone', 'topic', 'message',)
    widgets = {
      'name': TextInput(attrs={'placeholder': _('Name')}),
      'email': TextInput(attrs={'placeholder': _('Email Address')}),
      'phone': TextInput(attrs={'type': 'tel', 'placeholder':_('Phone Number')}),
      'message': Textarea(attrs={'placeholder': _('Please enter your message here'), 'class': 'form-control'})
    }

class ScheduleForm(ModelForm):
  class Meta:
    model = models.ScheduleModel
    fields = ('name', 'email', 'phone',)
    widgets = {
      'phone': TextInput(attrs={'type': 'tel', 'placeholder':_('Phone Number'),'class':'form-control'}),
      'name': TextInput(attrs={'placeholder': _('Name'), 'class': 'form-control'}),
      'email': TextInput(attrs={'placeholder': _('Email Address'), 'class':'form-control'}),
    }
  def clean_email(self):
    from django.core.exceptions import ValidationError
    email = self.cleaned_data['email']
    if email.split('@')[1] in INCOGNITO_LIST:
      raise ValidationError(_('Please use a valid work email address.'))
    return email


class PricingContactForm(ModelForm):
  DEVICE_COUNTS = (
    ('unknown', _('I am not sure'), '--'),
    ('100', '1 - 100 Devices', '1 - 1,000'),
    ('500', '101 - 500 Devices', '1,001 - 5,000'),
    ('1000', '501 - 1,000 Devices', '5,001 - 10K'),
    ('2500', '1,001 - 2,500 Devices', '10,001 - 25K'),
    ('5000', '2,501 - 5,000 Devices', '25,001 - 50K'),
    ('10000', '5,001 - 10K Devices', '50,001 - 100K'),
    ('25000', '10K - 25K', '100,001 - 250K'),
    ('25000plus', '25,001+ Devices', '250K+'),
  )

  class Meta:
    model = models.PricingContactModel
    fields = ('name', 'email', 'company', 'phone', 'country', 'device_count', 'slm_addon', 'power_monitoring_addon',
              'power_control_addon', 'referred_by_reseller', 'reseller_name',)
    widgets = {
      'phone': TextInput(attrs={'type': 'tel'}),
    }

  def clean_email(self):
    from django.core.exceptions import ValidationError
    email = self.cleaned_data['email']
    if email.split('@')[1] in INCOGNITO_LIST:
      raise ValidationError(_('Please use a valid work email address.'))
    return email

class FreeClientForm(ModelForm):
  class Meta:
    model = models.FreeClient
    fields = ('email','Subscribe','I_agree_to_EULA',)

class UpdateForm(ModelForm):
  class Meta:
    model = models.UpdateModel
    fields = ('email',)

  def clean_email(self):
    from django.core.exceptions import ValidationError
    email = self.cleaned_data['email']
    if email.split('@')[1] in INCOGNITO_LIST:
      raise ValidationError(_('Please use a valid work email address.'))
    return email

class BetaSignUpForm(ModelForm):
  class Meta:
    model = models.BetaSignUp
    fields = ('name', 'email',)
    widgets = {
      'name': TextInput(attrs={'placeholder': _('Name')}),
    }

  def clean_email(self):
    from django.core.exceptions import ValidationError
    email = self.cleaned_data['email']
    if email.split('@')[1] in INCOGNITO_LIST:
      raise ValidationError(_('Please use a valid work email address.'))
    return email

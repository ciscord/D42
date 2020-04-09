# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class CustomForm(object):
  """
  Inherit with forms.Form or forms.ModelForm
  For example:
      class AnyForm(forms.Form, CustomForm):
          pass

      class AnyModelForm(forms.ModelForm, CustomForm):
          pass
  """

  def render_errors(self):
    if not self.errors:
      return ""
    output = [u'<div class="alert-message block-message error">', u'<a class="close" href="#">×</a>',
              u'<p><strong>%s</strong></p><ul>' % _('You got an error!')]
    for field, error in self.errors.items():
      output.append(u'<li><strong>%s</strong> %s</li>' % (field.title(), error[0]))
    output.append(u'</ul></div>')
    return mark_safe(u'\n'.join(output))

  def as_div(self):
    output = []
    for boundfield in self:  # see original Form class __iter__ method
      row_template = u'''
            <div class="clearfix %(div_class)s">
                %(label)s
                <div class="input">
                    %(field)s
                    <span class="help-block">%(help_text)s </span>
                </div>
            </div>
            '''
      row_dict = {
        "div_class": "",
        "required_label": "",
        "field": boundfield.as_widget(),
        "label": boundfield.label_tag(),
        "help_text": boundfield.help_text,
      }

      if boundfield.errors:
        row_dict["div_class"] = "error"
        boundfield.field.widget.attrs["class"] = "error"

      output.append(row_template % row_dict)
    return mark_safe(u'\n'.join(output))

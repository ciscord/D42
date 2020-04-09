from dateutil import parser as dateparser
from django import template
from django.template import Library, Node, Variable, loader
from django.template.context import Context
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.conf import settings
from django.utils import translation
from .. import not_translated

register = Library()

# --------------------
# template helpers
# --------------------
@register.assignment_tag(takes_context=True)
def lang_code(context):
  return context['request'].LANGUAGE_CODE

@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
  url = path = context['request'].path
  protocal = 'http' + ('','s')[context['request'].is_secure()]
  url_parts = resolve(path)
  context_lang = translation.get_language()
  try:
    translation.activate(lang)
    url = reverse(url_parts.view_name, kwargs=url_parts.kwargs)
  finally:
    translation.activate(context_lang)

  return "%s" % url

@register.tag
def setting ( parser, token ):
    try:
        tag_name, option = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents[0]
    return SettingNode( option )

class SettingNode ( template.Node ):
    def __init__ ( self, option ):
        self.option = option

    def render ( self, context ):
        # if FAILURE then FAIL silently
        try:
            return str(settings.__getattr__(self.option))
        except:
            return ""

@register.filter
def get_key(dictionary, key):
  try:
    return [item[0] for item in dictionary.items() if item[1] == key][0]
  except KeyError:
    return ''

@register.filter
def get_item(dictionary, key):
  try:
    return dictionary[key]
  except KeyError:
    return ''


# --------------------
# inclusion tags
# --------------------
@register.inclusion_tag('base/landing.html', takes_context=True)
def landingpage(context):
  return {'page': context['page']}


@register.inclusion_tag('base/navigation.html', takes_context=False)
def navigation():
  sections = [
    "Product",
    "Features",
    "Customers",
    "Support",
    "Company",
  ]

  return {
    'site_sections': sections,
  }


class PartialTemplateNode(Node):
  def __init__(self, template_name, context_item):
    self.template_name = template_name
    self.context_item = Variable(context_item)

  def render(self, context):
    template = loader.get_template(self.template_name)
    item = self.context_item.resolve(context)
    template_context = Context({
      'item': item
    })
    return template.render(template_context)


class TranslatedURL(template.Node):
    def __init__(self, language):
        self.language = language

    def render(self, context):
        view = resolve(context['request'].path)
        request_language = translation.get_language()
        translation.activate(self.language)
        url = reverse(view.urlconf_name, args=view.args, kwargs=view.default_kwargs)
        translation.activate(request_language)
        return url

@register.simple_tag(name='translate_url', takes_context=True)
def do_translate_url(context, lang=None, *args, **kwargs):
    try:
        path = "/"
        if context and context.has_key('request') and any(context['request'].path):
            path = context['request'].path
        for nt in not_translated:
            if nt in path:
                return path
        url_parts = resolve(path)
        url = path
        cur_language = translation.get_language()
        try:
            translation.activate(lang)
            url = reverse(url_parts.view_name, kwargs=url_parts.kwargs)
        finally:
            translation.activate(cur_language)
        return "%s" % url
    except:
        return None

@register.filter(name='to_date')
def to_date(value):
    return dateparser.parse(value)

@register.filter(name='lt')
def lt(a,b):
  return a < b

@register.filter(name='gt')
def gt(a,b):
  return a > b

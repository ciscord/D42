import re

from django.template import Context, Library, Node, Variable, TemplateSyntaxError
from django.template.loader import get_template

register = Library()


class PartialNode(Node):
  def __init__(self, partial, params):
    self.partial = partial
    self.params = params

  def render(self, context):
    context_params = {}

    for k, v in self.params.items():
      context_params[k] = Variable(v).resolve(context)
      t = get_template('%s' % self.partial)

    return t.render(Context(context_params))


@register.tag
def include_partial(parser, token):
  """
      Include a template snippet (partial) with it's own context
      Heavily based on http://freeasinbeard.org/post/107743420/render-partial-in-django
  """

  __doc__ = '{% include_partial "path/to/template.html" field=form.name label="string" arg3=foo %}'

  bits = token.split_contents()

  if len(bits) == 1:
    raise TemplateSyntaxError('Accepted format: %s' % __doc__)

  params = {}
  try:
    tag_name, partial = bits[:2]
    if partial.startswith('"'):
      partial = partial[1:-1]

    for bit in bits[2:]:
      s, key, value = re.split('^(\w+)=', bit)
      params[key] = value

  except ValueError:
    raise TemplateSyntaxError('Accepted format: %s' % __doc__)

  return PartialNode(partial, params)

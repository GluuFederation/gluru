import os
import string
import markdown
from hashlib import md5
from urllib import urlencode

from django import template

from tickets.utils import generate_ticket_link

register = template.Library()


@register.filter(name='markdownify')
def markdownify(text):
    # safe_mode governs how the function handles raw HTML
    return markdown.markdown(text, safe_mode='escape', extensions=['markdown.extensions.fenced_code'])


@register.simple_tag
def get_gravatar(email, size=80, rating='g', default=None):
    """ Return url for a Gravatar. From Zinnia blog. """
    url = 'https://secure.gravatar.com/avatar/{0}.jpg'
    if email:
        url = url.format(md5(email.strip().lower()).hexdigest())
    else:
        url = url.format('00000000000000000000000000000000')
    options = {'s': size, 'r': rating}
    if default:
        options['d'] = default

    url = '%s?%s' % (url, urlencode(options))
    return url.replace('&', '&amp;')


@register.filter(name='multiple_output_value')
def multiple_output_value(value, type):
    """ Get the right value """
    nv = '-'
    if value:
        all_values = string.split(value,',')
        values_list = []
        opt = eval(type)

        for i in opt:
            if str(i[0]) in all_values:
                values_list.append(i[1] + ' - yes')
            else:
                values_list.append(i[1] + ' - no')

        nv = '<br />'.join(values_list)

    return nv


@register.filter(name='filename')
def filename(value):
    try:
        return os.path.basename(value.file.name)
    except:
        return value


@register.filter(name='linkify')
def get_link(value):
    return generate_ticket_link(value)

import os
import urllib
import hashlib

from django.templatetags.static import static
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import apnumber, intcomma, intword, naturalday, naturaltime, ordinal
from django.template.defaultfilters import time, date

from jinja2 import Environment

def cravatar(email, size=100):
    return "https://cravatar.cn/avatar/{}?{}".format(
        hashlib.md5(email.lower().encode('utf-8')).hexdigest(),
        urllib.parse.urlencode({'s': str(size)})
    )

def basename(path):
    return os.path.basename(path)

def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            "cravatar": cravatar,
        }
    )
    env.filters.update({
        'apnumber': apnumber,
        'intcomma': intcomma,
        'intword': intword,
        'naturalday': naturalday,
        'naturaltime': naturaltime,
        'ordinal': ordinal,
        'basename': basename,
        'time': time,
        'date': date,
    })
    return env

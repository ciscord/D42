from django.conf import settings
import not_translated

valid_language_codes = [lang[0] for lang in settings.LANGUAGES]


def get_d42_language(request):
    if not request.LANGUAGE_CODE or not request.LANGUAGE_CODE in valid_language_codes:
        return "en"
    else:
        return request.LANGUAGE_CODE


def set_d42_language(request):
    lang = get_d42_language(request)
    return {'D42_LANGUAGE': lang}


def get_d42_locale_url(request):
    lang = get_d42_language(request)
    if lang == 'en':
        return ""
    else:
        return "/" + lang


def set_d42_locale_url(request):
    url_prep = get_d42_locale_url(request)
    return {'URL_PREPEND': url_prep}


def site_url(request):
    url_domain = settings.STATIC_DOMAIN
    return {'STATIC_DOMAIN': url_domain}

def check_translated(request):
    translated = True
    try:
        for nt in not_translated:
            if nt in request.path:
                translated = False
    except:
        pass

    return {'D42_TRANSLATED': translated}

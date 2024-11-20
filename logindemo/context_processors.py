from logindemo.config import WEB_NAME, WEB_COMPANY, WEB_URL, WEB_DESCRIPTION
from logindemo.settings import STATIC_URL, MEDIA_URL

def siteinfo(request):
    result = {'WEB_NAME': WEB_NAME,
              'WEB_COMPANY': WEB_COMPANY,
              'WEB_URL': WEB_URL,
              'WEB_DESCRIPTION': WEB_DESCRIPTION,
              'STATIC_URL': STATIC_URL,
              'MEDIA_URL': MEDIA_URL,
              }
    return result

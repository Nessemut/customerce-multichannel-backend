from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .. import settings


@csrf_exempt
def script(req):
    with open('{}{}loadChat.js'.format(settings.APP_ABSOLUTE_PATH, settings.STATIC_URL), "rb") as f:
        return HttpResponse(f.read(), content_type="application/javascript")

from ..model.shop import Shop
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from .. import settings
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def script(req):
    with open('{}{}loadChat.js'.format(settings.APP_ABSOLUTE_PATH, settings.STATIC_URL), "rb") as f:
        return HttpResponse(f.read(), content_type="application/javascript")

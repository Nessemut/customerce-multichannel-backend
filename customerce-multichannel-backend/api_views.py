from django.http import JsonResponse, HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

from .model import Shop, Notification, Faq
from .shopify_api_client import ShopifyApiClient

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import settings


class ShopView(APIView):

    @staticmethod
    def chat_info(req, shopname):
        try:
            shop = Shop.objects.get(name=shopname)
            res = {
                'id': shop.id,
                'name': shop.name,
                'facebook_active': shop.facebook_active,
                'whatsapp_active': shop.whatsapp_active,
                'email_active': shop.email_active,
                'panel_color': shop.panel_color,
                'panel_title': shop.panel_title
            }

            if shop.facebook_active:
                res['facebook_page'] = shop.facebook_page
            if shop.email_active:
                res['email'] = shop.email
            if shop.whatsapp_active:
                res['whatsapp_number'] = shop.whatsapp_number
                res['whatsapp_text'] = shop.whatsapp_text
            return JsonResponse({'shop': res})
        except Shop.DoesNotExist:
            return JsonResponse({'error': '{} does not exist'.format(shopname)})

    def enable_button(self, req, **shop_id):
        # TODO: move this to frontend
        if req.GET['enabled'] is not None:
            enable = req.GET['enabled'] == 'true'
            shop = Shop.objects.get(id=shop_id)
            if enable and not shop.app_enabled:
                api = ShopifyApiClient(shop)
                api.add_script_tag()
            elif not enable and shop.app_enabled:
                api = ShopifyApiClient(shop)
                api.remove_script_tag()
            return HttpResponse(status=200)
        return JsonResponse({'error': 'Choice not provided'}, status=400)

    @staticmethod
    def get_avatar_image(req, shopname):
        shop = Shop.objects.get(name=shopname)
        return HttpResponse(shop.get_image(), content_type="image/png")


class NotificationApi(APIView):

    @staticmethod
    def get_notification(notification_id):
        notification = Notification.objects.get(pk=notification_id)
        res = {'notification': notification.serialize()}
        return res

    @staticmethod
    def get_all(shop_id):
        notif_list = Notification.objects.filter(shop_id=shop_id)
        notif_array = []
        for notification in notif_list:
            notif_array.append(notification.serialize())
        res = {"notifications": notif_array}
        return res


class FaqAPI(APIView):
    pass


class ScriptTagApi(APIView):

    @staticmethod
    def script(req):
        with open('{}{}loadChat.js'.format(settings.APP_ABSOLUTE_PATH, settings.STATIC_URL), "rb") as f:
            return HttpResponse(f.read(), content_type="application/javascript")


class EmailApi(APIView):
    @csrf_exempt
    def send(self, req):
        # TODO: implement email send
        form = req.POST
        try:
            return HttpResponse(
                'Succesful dummy call to send email to {} from {}'.format(form['shop'], form['email']),
                status=200
            )
        except Exception:
            return HttpResponse('Something went wrong', status=400)

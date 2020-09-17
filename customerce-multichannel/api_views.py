from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import settings
from .models import Shop, Notification, Faq
from .shopify_api_client import ShopifyApiClient


class ShopApi:

    def chat_info(self, shopname):
        try:
            shop = Shop.objects.get(name=shopname)
            return JsonResponse(shop.serialize())
        except Shop.DoesNotExist:
            return JsonResponse({'error': '{} does not exist'.format(shopname)}, status=404)

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

    def get_avatar_image(self, req, shopname):
        shop = Shop.objects.get(name=shopname)
        return HttpResponse(shop.get_image(), content_type="image/png")


class NotificationApi:

    def get_notification(self, notification_id):
        notification = Notification.objects.get(pk=notification_id)
        res = {'notification': notification.serialize()}
        return JsonResponse(res)

    def get_all(self, shop_id):
        notifs = Notification.objects.filter(shop_id=shop_id)
        notif_list = []
        for notification in notifs:
            notif_list.append(notification.serialize())
        res = {"notifications": notif_list}
        return JsonResponse(res)


class FaqApi:

    def get_all(self, shop_id):
        faqs = Faq.objects.filter(shop_id=shop_id)
        faq_list = []
        for faq in faqs:
            faq_list.append(faq.serialize())
        res = {"notifications": faq_list}
        return JsonResponse(res)


class ScriptTagApi:

    @staticmethod
    def script(req):
        # TODO: we should generate the script on the go depending on working environment
        with open('{}{}loadChat.js'.format(settings.APP_ABSOLUTE_PATH, settings.STATIC_URL), "rb") as f:
            return HttpResponse(f.read(), content_type="application/javascript")


class EmailApi:
    @csrf_exempt
    def send(self, req):
        # TODO: implement email send
        form = req.POST
        return HttpResponse(
            'Succesful dummy call to send email to {} from {}'.format(form['shop'], form['email']),
            status=200
        )

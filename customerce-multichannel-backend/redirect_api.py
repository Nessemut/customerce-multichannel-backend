from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from . import settings
from model import Shop
from shopify_api_client import ShopifyApiClient


def confirm(req):
    name = req.GET['shop'].replace('.myshopify.com', '')
    shop = Shop.objects.get(name=name)
    api = ShopifyApiClient(shop)
    auth = req.GET['code']
    api.confirm_installation(auth)
    url = api.add_billing()
    return HttpResponseRedirect(url)


def install(req):
    name = req.GET['shop'].replace('.myshopify.com', '')
    try:
        shop = Shop(name)
        shop.save()
    except IntegrityError:
        shop = Shop.objects.get(name=name)
    api = ShopifyApiClient(req.META['HTTP_HOST'], shop)
    return HttpResponseRedirect(api.redirect_to_install_confirmation())


def redirect_to_installation(req, shopname):
    return HttpResponseRedirect('{}/install?shop={}'.format(req.META['HTTP_HOST'], shopname))


@csrf_exempt
def redirect(req):
    # TODO: thoroughly test this and catch probable errors
    if req.GET['shop'] is not None:
        name = req.GET['shop'].replace('.myshopify.com', '')
        try:
            shop = Shop.objects.get(name=name)
            shopify = ShopifyApiClient(shop)
            if shopify.token_valid():
                shopify.activate_billing()
                return HttpResponseRedirect('{}?shop={}&token={}'.format(
                    settings.FRONTEND_URL, name, shop.token))
            else:
                return redirect_to_installation(req, name)
        except Shop.DoesNotExist:
            return redirect_to_installation(req, name)

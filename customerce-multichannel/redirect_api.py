from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from . import settings
from .models import Shop
from .shopify_api_client import ShopifyApiClient

# TODO: fix bug that causes an infinite redirection loop when reinstalling the app


def confirm(req):
    name = req.GET['shop'].replace('.myshopify.com', '')
    shop = Shop.objects.get(name=name)
    api = ShopifyApiClient(req.META['HTTP_HOST'], shop)
    auth = req.GET['code']
    api.confirm_installation(auth)
    url = api.add_billing()
    shop.save()
    return HttpResponseRedirect(url)


def install(req):
    name = req.GET['shop'].replace('.myshopify.com', '')
    try:
        shop = Shop.objects.get(name=name)
        if not shop.billing_accepted:
            api = ShopifyApiClient(req.META['HTTP_HOST'], shop)
            return HttpResponseRedirect(api.redirect_to_install_confirmation())
        return HttpResponseRedirect('http://{}/redirect?shop={}'.format(
            req.META['HTTP_HOST'], name))
    except Shop.DoesNotExist:
        shop = Shop.objects.create()
        shop.name = name
        shop.save()
        api = ShopifyApiClient(req.META['HTTP_HOST'], shop)
        return HttpResponseRedirect(api.redirect_to_install_confirmation())


def redirect_to_installation(req, shopname):
    return HttpResponseRedirect('http://{}/install?shop={}'.format(req.META['HTTP_HOST'], shopname))


@csrf_exempt
def redirect(req):
    if req.GET['shop'] is not None:
        name = req.GET['shop'].replace('.myshopify.com', '')
        try:
            shop = Shop.objects.get(name=name)
            shopify_api = ShopifyApiClient(req.META['HTTP_HOST'], shop)
            if shopify_api.token_valid():
                shop.billing_accepted = True
                shop.save()
                shopify_api.activate_billing()
                return HttpResponseRedirect('http://{}?shop={}&token={}'.format(
                    req.META['HTTP_HOST'], name, shop.token))
            else:
                return redirect_to_installation(req, name)
        except Shop.DoesNotExist:
            return redirect_to_installation(req, name)

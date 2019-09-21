from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .. import settings
from ..model.shop import Shop
from ..service.shop_manager import get_shop, create_shop
from ..util.shopify_api import ShopifyApi


def confirm(req):
    name = req.GET['shop'].replace('.myshopify.com', '')
    shop = get_shop(name)
    api = ShopifyApi(shop)
    auth = req.GET['code']
    api.confirm_installation(auth)
    url = api.add_billing()
    return HttpResponseRedirect(url)


def install(req):
    name = req.GET['shop'].replace('.myshopify.com', '')
    try:
        shop = create_shop(name)
    except IntegrityError:
        shop = get_shop(name)
    api = ShopifyApi(shop)
    return HttpResponseRedirect(api.redirect_to_install_confirmation())


def redirect_to_installation(shopname):
    return HttpResponseRedirect('{}/install?shop={}'.format(settings.APP_URL, shopname))


@csrf_exempt
def redirect(req):
    # TODO: thoroughly test this and catch probable errors
    if req.GET['shop'] is not None:
        name = req.GET['shop'].replace('.myshopify.com', '')
        try:
            shop = get_shop(name)
            shopify = ShopifyApi(shop)
            if shopify.token_valid():
                shopify.activate_billing()
                return HttpResponseRedirect('{}?shop={}&token={}'.format(
                    settings.FRONTEND_URL, name, shop.token))
            else:
                return redirect_to_installation(name)
        except Shop.DoesNotExist:
            return redirect_to_installation(name)

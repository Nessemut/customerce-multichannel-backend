from django.http import JsonResponse, HttpResponse, QueryDict

from src.model.shop import Shop
from src.service.shop_manager import get_chat_info, get_merchant_info, get, get_image, save_image, update
from ..util.authentication import authenticate
from ..util.shopify_api import ShopifyApi
from django.views.decorators.csrf import csrf_exempt


def chat_info(req, shopname):
    try:
        shop = get_chat_info(shopname)
        return JsonResponse({'shop': shop})
    except Shop.DoesNotExist:
        return JsonResponse({'error': '{} does not exist'.format(shopname)})


@authenticate
def enable_button(req, **shop_id):
    if req.GET['enabled'] is not None:
        enable = req.GET['enabled'] == 'true'
        shop = get(shop_id)
        if enable and not shop.app_enabled:
            api = ShopifyApi(shop)
            api.add_script_tag()
        elif not enable and shop.app_enabled:
            api = ShopifyApi(shop)
            api.remove_script_tag()
        return HttpResponse(status=200)
    return JsonResponse({'error': 'Choice not provided'}, status=400)


@csrf_exempt
@authenticate
def post_avatar_image(req, **kwargs):
    if req.method == 'POST':
        file = req.FILES.get('image')
        save_image(file, kwargs['shop_id'])
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)


def get_avatar_image(req, shopname):
    return HttpResponse(get_image(shopname), content_type="image/png")


@csrf_exempt
@authenticate
def admin_crud(req, **kwargs):
    shop_id = str((kwargs['shop_id']))
    try:
        if req.method == 'GET':
            shop = get_merchant_info(shop_id)
            return JsonResponse({'shop': shop})
        elif req.method == 'PUT':
            form = QueryDict(req.body)
            try:
                update(form, shop_id)
            except KeyError:
                return JsonResponse({'error': 'Incomplete form'}, status=400)
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=405)
    except Exception as e:
        return HttpResponse(e.__cause__, status=400)

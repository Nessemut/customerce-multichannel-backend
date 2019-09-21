from django.http import JsonResponse, HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from ..util.authentication import authenticate, verify_object_ownership
from ..model.faq import Faq
from ..service.faq_manager import get_all, get_faq, create, update, delete


@csrf_exempt
def get_all_from_shop(req, shop_id):
    return JsonResponse(get_all(shop_id))


@csrf_exempt
@authenticate
def admin_post(req, **kwargs):
    shop_id = str(kwargs['shop_id'])
    if req.method != 'POST':
        return HttpResponse(status=405)
    try:
        form = QueryDict(req.body)
        create(form, shop_id)
    except Exception as e:
        return JsonResponse({'error': (str(e))}, status=400)
    return HttpResponse(status=201)


@csrf_exempt
@authenticate
def admin_crud_object(req, **kwargs):
    faq_id = kwargs['_id']
    shop_id = str(kwargs['shop_id'])
    if not verify_object_ownership(shop_id, faq_id, Faq):
        return JsonResponse({'error': 'You have no permisson to modify this resource'}, status=401)
    try:
        if req.method == 'GET':
            return JsonResponse(get_faq(faq_id))
        elif req.method == 'POST':
            return HttpResponse(status=405)
        elif req.method == 'PUT':
            form = QueryDict(req.body)
            update(form, faq_id)
            return HttpResponse(status=200)
        elif req.method == 'DELETE':
            delete(faq_id)
            return HttpResponse(status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
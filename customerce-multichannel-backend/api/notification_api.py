from django.http import JsonResponse, HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt

from ..model import Notification
from ..service.notification_manager import get_all, get_notification, create, update, delete


@csrf_exempt
def get_all_from_shop(req, shop_id):
    return JsonResponse(get_all(shop_id))


@csrf_exempt
def admin_post(req, **kwargs):
    shop_id = str(kwargs['shop_id'])
    if req.method != 'POST':
        admin_crud_object(req, **kwargs)
    try:
        form = QueryDict(req.body)
        create(form, int(shop_id))
    except Exception as e:
        return JsonResponse({'error': (str(e))}, status=400)
    return HttpResponse(status=201)


@csrf_exempt
def admin_crud_object(req, **kwargs):
    try:
        notification_id = kwargs['_id']
    except KeyError:
        return JsonResponse({'error': 'Resource not found'}, status=404)
    shop_id = str(kwargs['shop_id'])
    #if not verify_object_ownership(shop_id, notification_id, Notification):
    #    return JsonResponse({'error': 'You have no permisson to modify this resource'}, status=401)
    try:
        if req.method == 'GET':
            return JsonResponse(get_notification(notification_id))
        elif req.method == 'POST':
            return HttpResponse(status=405)
        elif req.method == 'PUT':
            form = QueryDict(req.body)
            update(form, notification_id)
            return HttpResponse(status=200)
        elif req.method == 'DELETE':
            delete(notification_id)
            return HttpResponse(status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

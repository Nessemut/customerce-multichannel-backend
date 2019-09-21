from base64 import b64decode
from django.http import JsonResponse, HttpResponse, QueryDict
from ..service.shop_manager import get_id, authentication_correct


def verify_object_ownership(shop_id, _id, cl):
    if _id.__class__ == dict:
        _id = _id['_id']
    try:
        is_owner = int(cl.objects.get(pk=_id).shop_id) == int(shop_id)
        return is_owner
    except cl.DoesNotExist:
        return False


def authenticate(func):

    def wrapper(req, **kwargs):

        try:
            authentication = str(b64decode(str(req.META['HTTP_AUTHORIZATION'][6:])))
            separator_index = authentication.index(':')
            shop = authentication[2:separator_index]
            token = authentication[separator_index+1:len(authentication)-1]

            if not authentication_correct(shop, token):
                return HttpResponse(status=401)
        except KeyError:
            return HttpResponse(status=401)
        try:
            _id = kwargs['_id']
            return func(req, shop_id=get_id(shop), _id=_id)
        except KeyError:
            return func(req, shop_id=get_id(shop))
    return wrapper

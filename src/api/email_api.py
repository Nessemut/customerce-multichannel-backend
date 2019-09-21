from django.http import JsonResponse, HttpResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def send(req):
    # TODO: implement email send
    form = req.POST
    try:
        return HttpResponse(
            'Succesful dummy call to send email to {} from {}'.format(form['shop'], form['email']),
            status=200
        )
    except Exception:
        return HttpResponse('Do this properly dude', status=400)

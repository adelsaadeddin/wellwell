from django.http import JsonResponse

from space.step6_methods_for_production import predict as model_predict
from django.core.mail import send_mail


def predict(request):
    lat, lng = float(request.GET.get('lat')), float(request.GET.get('lng'))
    result = model_predict(lat, lng)
    return JsonResponse({'result': result})


def contact(request):
    name, email, phone, subject, message = request.POST
    send_mail(subject, 'noreplay@wellwellwell.app', ['info@wellwellwell.app'], html_message="", fail_silently=False)

from django.http import JsonResponse

from space.step6_methods_for_production import predict as model_predict


def predict(request):
    lat, lng = float(request.GET.get('lat')), float(request.GET.get('lng'))
    result = model_predict(lat, lng)
    return JsonResponse({'result': result})

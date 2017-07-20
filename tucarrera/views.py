from cities_light.models import City
from django.http import JsonResponse


# Create your views here.

def cities(request, country):
    if request.method == "GET":
        data = City.objects.filter(country__code2__iexact=country).values("id", "display_name")

        return JsonResponse(list(data), safe=False)

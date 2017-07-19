from .models import RacePage
from django.http import JsonResponse

from datetime import datetime


# Create your views here.

def filter_events(request):
    if request.method == "GET":

        races = RacePage.objects.filter(
            date__gt=datetime.fromtimestamp(int(request.GET["start"])),
            date__lt=datetime.fromtimestamp(int(request.GET["end"])),
            distance__gt=int(request.GET["distance_min"]),
            distance__lt=int(request.GET["distance_max"]),
        ).values('title', 'date', 'url_path')

        events = []
        for race in list(races):
            race['start'] = race['date'].isoformat()
            race['className'] = "success"
            race['url'] = race['url_path'][9:]  # slices to remove '/carrera' # TODO make this work for all cases
            events.append(race)

    return JsonResponse(events, safe=False)

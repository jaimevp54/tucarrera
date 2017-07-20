from .models import RacePage
from django.http import JsonResponse

from datetime import datetime

from moneyed import Money, DOP


# Create your views here.

def filter_events(request):
    if request.method == "GET":

        races: RacePage = RacePage.objects.filter(
            date__gt=datetime.fromtimestamp(int(request.GET["start"])),
            date__lt=datetime.fromtimestamp(int(request.GET["end"])),
            distance__gte=int(request.GET["distance_min"]),
            distance__lte=int(request.GET["distance_max"]),
        ).exclude(
            cost__lt=Money(int(request.GET["cost_min"]), DOP),
        ).exclude(
            cost__gt=Money(int(request.GET["cost_max"]), DOP),
        )

        if request.GET["city"] != "0":
            races = races.filter(city__id=int(request.GET["city"]))

        if request.GET["scope"] != "all":
            races = races.filter(is_international=True if request.GET["scope"] == "international" else False)

        events = []
        for race in list(races.values('title', 'date', 'url_path')):
            race['start'] = race['date'].isoformat()
            race['className'] = "success"
            race['url'] = race['url_path'][9:]  # slices to remove '/carrera' # TODO make this work for all cases
            events.append(race)

    return JsonResponse(events, safe=False)

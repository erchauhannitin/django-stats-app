from django.http import JsonResponse
from statreports.models import AlarmRow, ClientParentRow
from django.shortcuts import render
from django.db.models import Count


def json_example(request):
    return render(request, 'statreports/json_example.html')


def chart_data(request):
    dataset = ClientParentRow.objects \
        .values('latency') \
        .exclude(latency=0) \
        .annotate(total=Count('latency')) \
        .order_by('latency')

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Ticket Class'},
        'series': [{
            'name': 'Embarkation Port',
            'data': list(map(lambda row: {'name': row['latency'], 'y': row['total']}, dataset))
        }]
    }

    return JsonResponse(chart)

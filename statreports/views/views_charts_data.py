from django.http import JsonResponse
from statreports.models import CharsRow, ClientParentRow
from django.shortcuts import render
from django.db.models import Count, Sum


def json_example(request):
    return render(request, 'statreports/json_example.html')


def chart_data(request):
    dataset = CharsRow.objects \
        .values('error') \
        .exclude(error='') \
        .annotate(totalSum=Sum('count')) \
        .annotate(totalCount=Count('count')) \
        .filter(totalSum__gte=100000) \
        .order_by('error')

    chart = {
        'chart': {'type': 'variablepie'},
        'title': {'text': 'Exception aggregation and percentage'},
        'series': [{
            'name': 'Exception type',
            'data': list(map(lambda row: {'name': row['error'], 'y': row['totalSum'], 'z': row['totalCount']}, dataset))
        }]
    }

    return JsonResponse(chart)

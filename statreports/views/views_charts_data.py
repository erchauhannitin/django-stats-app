from django.http import JsonResponse
from statreports.models import CharsRow, ClientParentRow
from django.shortcuts import render
from django.db.models import Count


def json_example(request):
    return render(request, 'statreports/json_example.html')


def chart_data(request):
    dataset = CharsRow.objects \
        .values('error') \
        .exclude(error='') \
        .annotate(total=Count('error')) \
        .order_by('error')

    print(dataset)

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Exception aggregation and percentage'},
        'series': [{
            'name': 'Exception type',
            'data': list(map(lambda row: {'name': row['error'], 'y': row['total']}, dataset))
        }]
    }

    return JsonResponse(chart)

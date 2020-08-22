from django.http import JsonResponse
from statreports.models import CharsRow
from django.shortcuts import render
from django.db.models import Count, Sum
from statreports.forms import ChartTypeForm


def json_char_data(request):
    context = {}
    form = ChartTypeForm(request.POST)
    context['form'] = form

    request.session['chart_type'] = request.POST.get('filter_by')
    return render(request, 'statreports/json_char_data.html', context)


def chart_data(request):

    chart_type = request.session.get('chart_type')
    dataset = CharsRow.objects \
        .values('error') \
        .exclude(error='') \
        .annotate(totalSum=Sum('count')) \
        .annotate(totalCount=Count('count')) \
        .filter(totalSum__gte=100000) \
        .order_by('error')

    chart = {
        'chart': {'type': chart_type, 'options3d': {
            'enabled': 'true',
            'alpha': '45',
            'beta': '0',
            'depth': '50',
            'viewDistance': '25'
        }},
        'plotOptions': {
            'pie': {
                'innerSize': '100',
                'depth': '45',
            }
        },
        'title': {'text': 'Exception aggregation and percentage'},
        'series': [{
            'name': 'Exception type',
            'data': list(map(lambda row: {'name': row['error'], 'y': row['totalSum'], 'z': row['totalCount']}, dataset))
        }]
    }

    return JsonResponse(chart)

from django.http import JsonResponse
from statreports.models import ClientParentRow
from django.shortcuts import render
from django.db.models import Count, Sum
from statreports.forms import ChartTypeForm


def clientparent_chart(request):
    context = {}
    form = ChartTypeForm(request.POST)
    context['form'] = form

    request.session['chart_type'] = request.POST.get('filter_by')
    return render(request, 'statreports/clientparent_summary.html', context)


def clientparent_json(request):

    chart_type = request.session.get('chart_type')
    dataset = ClientParentRow.objects \
        .values('latency') \
        .exclude(errors=0) \
        .filter(errors__gte=100000) \
        .order_by('latency')

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
            'colorByPoint': 'true',
            'data': list(map(lambda row: {'name': row['latency'], 'y': row['errors'], 'z': row['latency']}, dataset))
        }]
    }

    return JsonResponse(chart)

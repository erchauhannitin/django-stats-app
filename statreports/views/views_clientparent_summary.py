from django.http import JsonResponse
from statreports.models import ClientParentRow
from django.shortcuts import render
from statreports.forms import ChartTypeForm


def clientparent_chart(request):
    context = {}
    form = ChartTypeForm(request.POST)
    context['form'] = form

    request.session['chart_type'] = request.POST.get('filter_by')
    return render(request, 'statreports/clientparent_summary.html', context)


def clientparent_json(request):

    chart_type = request.session.get('chart_type')
    dataset = ClientParentRow.objects.order_by('-count')[0:5]
    dataset2 = ClientParentRow.objects.order_by('-errors')[0:5]
    dataset3 = ClientParentRow.objects.order_by('-latency')[0:5]

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
        'title': {'text': 'Problematic clients'},
        'series': [{
            'name': 'Client count',
            'colorByPoint': 'true',
            'data': list(map(lambda row: {'name': row.name, 'y': row.count}, dataset))
        },
            {
            'name': 'Client errors',
            'colorByPoint': 'true',
            'data': list(map(lambda row: {'name': row.name, 'y': row.errors}, dataset2))
        },
            #     {
            #     'name': 'Client latency',
            #     'colorByPoint': 'true',
            #     'data': list(map(lambda row: {'name': row.name, 'y': int(row.latency)}, dataset3))
            # }
        ]
    }

    return JsonResponse(chart)

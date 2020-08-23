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

    chart = {
        'chart': {'type': chart_type},
        'title': {'text': 'Problematic clients'},
        'series': [{
            'name': 'Client Name',
            'colorByPoint': 'true',
            'data': list(map(lambda row: {'name': row.name, 'y': row.count}, dataset))
        }]
    }

    return JsonResponse(chart)

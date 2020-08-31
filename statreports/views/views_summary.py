from django.http import JsonResponse
from statreports.models import ClientParentRow
from django.shortcuts import render
from django.db.models import Count, Sum
from statreports.forms import ChartTypeForm


def summary(request):

    context = {}

    criticalRows = ClientParentRow.objects \
        .filter(timeOuts__gte=100, errors__gte=100) \
        .order_by('errors')

    highRows = ClientParentRow.objects \
        .filter(errors__range=(1, 100)) \
        .order_by('errors')

    mediumRows = ClientParentRow.objects \
        .exclude(errors=0) \
        .filter(errors__lte=10) \
        .order_by('errors')

    context['criticalRows'] = criticalRows
    context['highRows'] = highRows
    context['mediumRows'] = mediumRows

    return render(request, "statreports/summary.html", context)

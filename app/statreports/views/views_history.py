from django.http import JsonResponse
from statreports.models import ClientParentHistory
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from statreports.forms import ChartTypeForm


def history(request):

    context = {}

    criticalRows = ClientParentHistory.objects \
        .filter(Q(timeOuts__gte=100) | Q(errors__gte=100) | Q(latency__gte=1000)) \
        .order_by('errors')

    highRows = ClientParentHistory.objects \
        .filter(Q(errors__range=(10, 100)) | Q(timeOuts__range=(10, 100))) \
        .order_by('errors')

    mediumRows = ClientParentHistory.objects \
        .exclude(errors=0) \
        .filter(Q(timeOuts__lte=10) | Q(errors__lte=10)) \
        .order_by('errors')

    context['criticalRows'] = criticalRows
    context['highRows'] = highRows
    context['mediumRows'] = mediumRows

    return render(request, "statreports/summary.html", context)

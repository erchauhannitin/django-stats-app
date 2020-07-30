from django.http import HttpResponse
from .models import ReportRow
from django.shortcuts import render, redirect
import re
from django.core.paginator import Paginator, EmptyPage


def all(request):
    lines = open("./statreports/input/input.txt", 'r').read()
    blocks = lines.split("\n\n")
    dest = None

    for block in blocks:

        titles = block.split("\n")
        dest = open(titles[0] + '.txt', 'w')
        dest.write(block)
        dest.close()

    file = open('./client.txt', 'r').readlines()
    title = file.pop(0)
    timeStamp = file.pop(0)
    header = file.pop(0)

    ReportRow.objects.all().delete()

    for line in file:
        words = re.split(r'  +', line.lstrip())
        NAME, ADDRESS, ACTIVE, INACTIVE, MAX_ACTIVE, COUNT, ERRORS, TIMEOUTS, LATENCY, PEAK_LATENCY, THROUGHPUT = [
            i for i in words]
        row = ReportRow(name=NAME, address=ADDRESS, active=ACTIVE, inActive=INACTIVE, maxActive=MAX_ACTIVE,
                        count=COUNT, errors=ERRORS, timeOuts=TIMEOUTS, latency=LATENCY, peakLatency=PEAK_LATENCY, throughPut=THROUGHPUT)
        row.save()

    rows = ReportRow.objects.order_by('-count')

    context = {'rows': rows, 'header': header,
               'title': title, 'timeStamp': timeStamp}
    return render(request, 'statreports/index.html', context)

from django.http import HttpResponse
from .models import ClientRow, ServerRow
from django.shortcuts import render, redirect
import re
from django.core.paginator import Paginator, EmptyPage
from django.db.utils import OperationalError


def all(request):
    lines = open("./statreports/input/input.txt", 'r').read()
    blocks = lines.split("\n\n")
    dest = None

    for block in blocks:

        titles = block.split("\n")
        dest = open(titles[0] + '.txt', 'w')
        dest.write(block)
        dest.close()

 
    try:
        ClientRow.objects.all().delete()
        #ServerRow.objects.all().delete()
    except OperationalError:
        pass  # happens when db doesn't exist yet, views.py should be

    clientFile = open('./client.txt', 'r').readlines()
    title = clientFile.pop(0)
    timeStamp = clientFile.pop(0)
    header = clientFile.pop(0)

    for line in clientFile:
        words = re.split(r'  +', line.lstrip())
        NAME, ADDRESS, ACTIVE, INACTIVE, MAX_ACTIVE, COUNT, ERRORS, TIMEOUTS, LATENCY, PEAK_LATENCY, THROUGHPUT = [
            i for i in words]
        clientRow = ClientRow(name=NAME, address=ADDRESS, active=ACTIVE, inActive=INACTIVE, maxActive=MAX_ACTIVE,
                        count=COUNT, errors=ERRORS, timeOuts=TIMEOUTS, latency=LATENCY, peakLatency=PEAK_LATENCY, throughPut=THROUGHPUT)
        try:
            clientRow.save()
        except OperationalError:
            pass #Ingore errors

    serverFile = open('./server.txt', 'r').readlines()
    title = serverFile.pop(0)
    timeStamp = serverFile.pop(0)
    header = serverFile.pop(0)

    for line in serverFile:
        words = re.split(r'  +', line.lstrip())
        NAME, ADDRESS, ACTIVE, MAX_ACTIVE, COUNT, ERRORS, LATENCY, PEAK_LATENCY, THROUGHPUT = [
            i for i in words]
        serverRow = ServerRow(name=NAME, address=ADDRESS, active=ACTIVE, maxActive=MAX_ACTIVE,
                        count=COUNT, errors=ERRORS, latency=LATENCY, peakLatency=PEAK_LATENCY, throughPut=THROUGHPUT)
        try:
            print(serverRow)
            serverRow.save()
        except OperationalError:
            pass #Ingore errors

    clientRows = ClientRow.objects.order_by('-count')
    serverRows = ServerRow.objects.order_by('-count')

    context = {'clientRows': clientRows, 
               'serverRows': serverRows, 
               'header': header,
               'title': title, 
               'timeStamp': timeStamp
               }
    return render(request, 'statreports/index.html', context)

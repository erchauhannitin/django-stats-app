from django.http import HttpResponse
from statreports.models import ClientRow, ServerRow, AlarmRow, ClientParentRow, ClientParentHistory
from django.shortcuts import render, redirect
import re
from django.db.utils import OperationalError
from statreports.forms import InputStatsFileForm
import shutil
import os
from django.contrib import messages
from django.db import transaction


def stats(request):

    clientRows = ClientRow.objects.order_by('-count')
    clientParentRows = ClientParentRow.objects.order_by('-count')
    serverRows = ServerRow.objects.order_by('-count')
    alarmRows = AlarmRow.objects.order_by('-module')

    context = {'clientRows': clientRows,
               'serverRows': serverRows,
               'alarmRows': alarmRows,
               'clientParentRows': clientParentRows
               }
    return render(request, 'statreports/stats.html', context)


def home_stat(request):
    context = {}
    if request.POST:
        form = InputStatsFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request)
            context['form'] = form
            return render(request, "statreports/home.html", context)
        else:
            context['form'] = form
            return render(request, "statreports/home.html", context)
    else:
        form = InputStatsFileForm()
        context['form'] = form
        return render(request, "statreports/home.html", context)


def handle_uploaded_file(request):
    f = request.FILES["input_Stats_File"]
    try:
        with open('./statreports/input/'+f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            lines = open('./statreports/input/'+f.name, 'r').read()
        blocks = lines.split("\n\n")
        dest = None

        clearsPreviousOutput(request)

        for block in blocks:

            titles = block.split("\n")
            if titles[0] == '':
                shutil.rmtree('./statreports/input/')
                os.makedirs('./statreports/input/')
                raise ValueError(
                    'Input file is not correct, check if it is valid statistics report')
            dest = open('./statreports/output/'+titles[0] + '.txt', 'w')
            dest.write(block)
            dest.close()

    except ValueError:
        print('Input file is not correct, check if it is valid statistics report')
        messages.add_message(request, messages.ERROR,
                             'Invalid input stats file')

    handleClient(request)
    handleServer(request)
    handleAlarm(request)


def clearsPreviousOutput(request):
    try:
        shutil.rmtree('./statreports/output/')
    except FileNotFoundError:
        pass

    try:
        os.makedirs('./statreports/output/')
    except OSError:
        pass

    try:
        ClientRow.objects.all().delete()
        ServerRow.objects.all().delete()
        AlarmRow.objects.all().delete()
        ClientParentRow.objects.all().delete()
    except OperationalError:
        pass


def handleClient(request):
    try:
        clientFile = open('./statreports/output/client.txt', 'r').readlines()
        title = clientFile.pop(0)
        timeStamp = clientFile.pop(0).replace('since ', '')
        header = clientFile.pop(0)

        with transaction.atomic():
            for line in clientFile:
                if(line.startswith(' ')):
                    words = re.split(r'  +', line.lstrip())
                    NAME, ADDRESS, ACTIVE, INACTIVE, MAX_ACTIVE, COUNT, ERRORS, TIMEOUTS, LATENCY, PEAK_LATENCY, THROUGHPUT = [
                        i for i in words]
                    clientRow = ClientRow(parentName=iteratedParentName, name=NAME, address=ADDRESS, active=ACTIVE,
                                          count=COUNT, errors=ERRORS, timeOuts=0 if TIMEOUTS == '-' else TIMEOUTS,
                                          latency=LATENCY.replace(' ms', ''), peakLatency=PEAK_LATENCY.replace(' ms', ''),
                                          throughPut=THROUGHPUT.replace('/s', ''))
                    saveData(clientRow)
                else:
                    words = re.split(r'  +', line)
                    iteratedParentName = words[0].replace(
                        'com.ericsson.em.am', 'c.e.e.a')
                    NAME, ADDRESS, ACTIVE, INACTIVE, MAX_ACTIVE, COUNT, ERRORS, TIMEOUTS, LATENCY, PEAK_LATENCY, THROUGHPUT = [
                        i for i in words]
                    clientParentRow = ClientParentRow(since=timeStamp, name=iteratedParentName, address=ADDRESS, active=ACTIVE, inActive=INACTIVE,
                                                      maxActive=MAX_ACTIVE, count=COUNT, errors=ERRORS, timeOuts=0 if TIMEOUTS == '-' else TIMEOUTS,
                                                      latency=LATENCY.replace(' ms', ''), peakLatency=PEAK_LATENCY.replace(' ms', ''),
                                                      throughPut=THROUGHPUT.replace('/s', ''))

                    clientParentHistory = ClientParentHistory(
                        since=timeStamp, name=iteratedParentName, address=ADDRESS, active=ACTIVE, inActive=INACTIVE,
                        maxActive=MAX_ACTIVE, count=COUNT, errors=ERRORS, timeOuts=0 if TIMEOUTS == '-' else TIMEOUTS,
                        latency=LATENCY.replace(' ms', ''), peakLatency=PEAK_LATENCY.replace(' ms', ''),
                        throughPut=THROUGHPUT.replace('/s', ''))

                    saveData(clientParentRow)
                    saveData(clientParentHistory)

    except OSError:
        print('No client data found')
        pass


def handleServer(request):
    try:
        serverFile = open('./statreports/output/server.txt', 'r').readlines()
        title = serverFile.pop(0)
        timeStamp = serverFile.pop(0)
        header = serverFile.pop(0)

        for line in serverFile:
            if(line.startswith(' ')):
                words = re.split(r'  +', line.lstrip())
                NAME, ADDRESS, ACTIVE, MAX_ACTIVE, COUNT, ERRORS, LATENCY, PEAK_LATENCY, THROUGHPUT = [
                    i for i in words]
                serverRow = ServerRow(parentName=iteratedParentName, name=NAME, address=ADDRESS, active=ACTIVE, maxActive=MAX_ACTIVE,
                                      count=COUNT, errors=ERRORS, latency=LATENCY.replace(
                                          ' ms', ''),
                                      peakLatency=PEAK_LATENCY.replace(' ms', ''), throughPut=THROUGHPUT.replace('/s', ''))
                saveData(serverRow)
            else:
                words = re.split(r'  +', line)
                iteratedParentName = words[0].replace(
                    'com.ericsson.em.am', 'c.e.e.a')
    except OSError:
        print('No server data found')
        pass


def handleAlarm(request):
    try:
        alarmFile = open('./statreports/output/alarm.txt', 'r').readlines()
        title = alarmFile.pop(0)
        timeStamp = alarmFile.pop(0)
        header = alarmFile.pop(0)

        for line in alarmFile:
            words = re.split(r'  +', line.lstrip())
            NAME, MODULE, ID, DESCRIPTION, RAISED, LAST_RAISED, CLEARED, LAST_CLEARED = [
                i for i in words]
            alarmRow = AlarmRow(name=NAME, module=MODULE, id=ID, description=DESCRIPTION,
                                raised=RAISED, lastRaised=LAST_RAISED, cleared=CLEARED, lastCleared=LAST_CLEARED)
            saveData(alarmRow)
    except OSError:
        print('No alarm data found')
        pass


def saveData(row):
    try:
        row.save()
    except OperationalError:
        print('Unable to save data, probably not in correct format', row)
        pass

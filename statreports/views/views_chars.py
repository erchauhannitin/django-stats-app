from django.http import HttpResponse
from statreports.models import PathRow
from django.shortcuts import render, redirect
import re
from django.db.utils import OperationalError
from statreports.forms import InputStatsFileForm
import shutil
import os
from django.contrib import messages


def chars(request):

    pathRows = PathRow.objects.order_by('-count')

    context = {'pathRows': pathRows}
    return render(request, 'statreports/chars.html', context)


def home_char(request):
    context = {}
    if request.POST:
        form = InputFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request)
            context['form'] = form
            return render(request, "statreports/home.html", context)
        else:
            context['form'] = form
            return render(request, "statreports/home.html", context)
    else:
        form = InputFileForm()
        context['form'] = form
        return render(request, "statreports/home.html", context)


def handle_uploaded_file(request):

    clearsPreviousOutput(request)
    handlePath(request)


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
        PathRow.objects.all().delete()
    except OperationalError:
        pass


def handlePath(request):

    f = request.FILES["inputFile"]
    try:
        pathFile = open('./statreports/input/'+f.name, 'r').readlines()
        for line in pathFile:
            previousRow
            words = re.split(r'  +', line.lstrip())
            if(len(words) == 4):
                NAME, ERROR, COUNT, LAST_OCCURRENCE = [
                    i for i in words]
                pathRow, previousRow = PathRow(name=NAME, error=ERROR,
                                               count=COUNT, lastOccurence=LAST_OCCURRENCE)
                try:
                    pathRow.save()
                except OperationalError:
                    print(
                        'Unable to save char data, probably not in correct format', pathRow)
                    pass
            elif(len(words) == 3):
                ERROR, COUNT, LAST_OCCURRENCE = [
                    i for i in words]
                print('previous Row', previousRow)
                # pathRow = PathRow(previousRow['name']=NAME, error=ERROR,
                #                   count=COUNT, lastOccurence=LAST_OCCURRENCE)
                # try:
                #     pathRow.save()
                # except OperationalError:
                #     print(
                #         'Unable to save char data, probably not in correct format', pathRow)
                #     pass
    except OSError:
        print('No char data found')
        pass

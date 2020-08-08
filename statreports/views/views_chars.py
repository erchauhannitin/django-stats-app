from django.http import HttpResponse
from statreports.models import CharsRow
from django.shortcuts import render, redirect
import re
from django.db.utils import OperationalError
from statreports.forms import InputCharsFileForm
import shutil
import os
from django.contrib import messages


def chars(request):

    charsRows = CharsRow.objects.order_by('-count')

    context = {'charsRows': charsRows}
    return render(request, 'statreports/chars.html', context)


def home_char(request):
    context = {}
    if request.POST:
        form = InputCharsFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request)
            context['form'] = form
            return render(request, "statreports/home.html", context)
        else:
            context['form'] = form
            return render(request, "statreports/home.html", context)
    else:
        form = InputCharsFileForm()
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
        CharsRow.objects.all().delete()
    except OperationalError:
        pass


def handlePath(request):

    f = request.FILES["input_Chars_File"]
    try:
        with open('./statreports/input/'+f.name, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
            lines = open('./statreports/input/'+f.name, 'r').readlines()
            header = lines.pop(0)

        for line in lines:

            if(line.startswith(' ')):
                words = re.split(r'  +', line.lstrip())
                if(len(words) == 4):
                    NAME, ERROR, COUNT, LAST_OCCURRENCE = [
                        i for i in words]
                    charsRow = CharsRow(parentName=iteratedParentName, name=NAME, error=ERROR,
                                        count=COUNT, lastOccurence=LAST_OCCURRENCE)
                    previousRow = charsRow
                    try:
                        charsRow.save()
                    except OperationalError:
                        print(
                            'Unable to save char data, probably not in correct format', charsRow)
                        pass
                elif(len(words) == 3):
                    ERROR, COUNT, LAST_OCCURRENCE = [
                        i for i in words]
                    charsRow = CharsRow(parentName=iteratedParentName, name=previousRow.name, error=ERROR,
                                        count=COUNT, lastOccurence=LAST_OCCURRENCE)
                    try:
                        charsRow.save()
                    except OperationalError:
                        print(
                            'Unable to save char data, probably not in correct format', charsRow)
                        pass
            else:
                words = re.split(r'  +', line)
                iteratedParentName = words[0].replace(
                    'com.ericsson.em.am', 'c.e.e.a')

    except OSError:
        print('No char data found')
        pass

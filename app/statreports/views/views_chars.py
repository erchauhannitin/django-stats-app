from django.http import HttpResponse
from statreports.models import CharsRow, MenuCharsRow
from django.shortcuts import render, redirect
import re
from django.db.utils import OperationalError
from statreports.forms import InputCharsFileForm
import shutil
import os
from django.contrib import messages


def chars(request):

    charsRows = CharsRow.objects.order_by('-count')
    menuCharsRows = MenuCharsRow.objects.order_by('-count')

    context = {'charsRows': charsRows,
               'menuCharsRows': menuCharsRows}
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
        MenuCharsRow.objects.all().delete()
    except OperationalError:
        pass


def handlePath(request):

    files = request.FILES.getlist('input_Chars_File')
    for file in files:
        try:
            with open('./statreports/input/'+file.name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                lines = open('./statreports/input/'+file.name, 'r').readlines()
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
                        if(iteratedParentName == 'c.e.e.a.menu'):
                            menuCharsRow = MenuCharsRow(name=NAME, error=ERROR,
                                                        count=COUNT, lastOccurence=LAST_OCCURRENCE)
                            saveData(menuCharsRow)
                        else:
                            saveData(charsRow)
                    elif(len(words) == 3):
                        ERROR, COUNT, LAST_OCCURRENCE = [
                            i for i in words]
                        charsRow = CharsRow(parentName=iteratedParentName, name=previousRow.name, error=ERROR,
                                            count=COUNT, lastOccurence=LAST_OCCURRENCE)
                        if(iteratedParentName == 'c.e.e.a.menu'):
                            menuCharsRow = MenuCharsRow(name=previousRow.name, error=ERROR,
                                                        count=COUNT, lastOccurence=LAST_OCCURRENCE)
                            saveData(menuCharsRow)
                        else:
                            saveData(charsRow)

                else:
                    words = re.split(r'  +', line)
                    iteratedParentName = words[0].replace(
                        'com.ericsson.em.am', 'c.e.e.a')

        except OSError:
            print('No char data found')
            pass


def saveData(row):
    try:
        row.save()
    except OperationalError:
        print('Unable to save data, probably not in correct format', row)
        pass

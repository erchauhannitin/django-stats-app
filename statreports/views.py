from django.http import HttpResponse
from .models import ReportRow
from django.shortcuts import render, redirect
import re


class Entry(object):
    def __init__(self, NAME, ADDRESS, ACTIVE, INACTIVE, MAX_ACTIVE, COUNT, ERRORS, TIMEOUTS, LATENCY, PEAK_LATENCY, THROUGHPUT):
        super(Entry, self).__init__()
        self.NAME = NAME
        self.ADDRESS = ADDRESS
        self.ACTIVE = ACTIVE
        self.INACTIVE = INACTIVE
        self.MAX_ACTIVE = MAX_ACTIVE
        self.COUNT = COUNT
        self.ERRORS = ERRORS
        self.TIMEOUTS = TIMEOUTS
        self.LATENCY = LATENCY
        self.PEAK_LATENCY = PEAK_LATENCY
        self.THROUGHPUT = THROUGHPUT
        self.entries = []

    def __str__(self):
        return self.NAME + " " + self.ADDRESS + " " + self.COUNT + " " + self.ERRORS

    def __repr__(self):
        return self.__str__()


def stats(request):
    lines = open("./statreports/input/input.txt", 'r').read()
    blocks = lines.split("\n\n")
    dest = None

    for block in blocks:

        titles = block.split("\n")
        dest = open(titles[0] + '.txt', 'w')
        dest.write(block)
        dest.close()

    entries = []
    file = open('./client.txt', 'r').readlines()
    title = file.pop(0)
    timeStamp = file.pop(0)
    header = file.pop(0)

    for line in file:
        words = re.split(r'  +', line.lstrip())
        NAME, ADDRESS, ACTIVE, INACTIVE, MAX_ACTIVE, COUNT, ERRORS, TIMEOUTS, LATENCY, PEAK_LATENCY, THROUGHPUT = [
            i for i in words]
        entry = Entry(NAME, ADDRESS, ACTIVE, INACTIVE, MAX_ACTIVE,
                      COUNT, ERRORS, TIMEOUTS, LATENCY, PEAK_LATENCY, THROUGHPUT)
        entries.append(entry)

    maxEntry = max(entries, key=lambda entry: entry.COUNT)
    print(maxEntry)

    rows = ReportRow.objects.order_by('name')
    context = {'rows': rows}
    return render(request, 'statreports/index.html', context)

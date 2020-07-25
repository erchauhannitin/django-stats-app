from django.http import HttpResponse
from .models import ReportRow
from django.shortcuts import render, redirect


class Entry(object):
    def __init__(self, NAME, SIZE, MAXSIZE):
        super(Entry, self).__init__()
        self.NAME = NAME
        self.SIZE = SIZE
        self.MAXSIZE = MAXSIZE
        self.entries = []

    def __str__(self):
        return self.NAME + " " + self.SIZE

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
    file = open('./cluster.txt', 'r').readlines()
    title = file.pop(0)
    timeStamp = file.pop(0)
    header = file.pop(0)

    for line in file:
        words = line.split()
        NAME, SIZE, MAXSIZE = [i for i in words]
        entry = Entry(NAME, SIZE, MAXSIZE)
        entries.append(entry)

        maxEntry = max(entries, key=lambda entry: entry.NAME)
        print(maxEntry)

    #rows = ReportRow.objects.order_by('name')
    #context = {'rows': rows}
    # return render(request, 'statreports/index.html', context)
    return HttpResponse('Stats')

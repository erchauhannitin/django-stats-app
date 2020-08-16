from django.db import models


class ClientRow(models.Model):
    parentName = models.CharField(max_length=50)
    name = models.CharField(max_length=20, primary_key=True)
    address = models.CharField(max_length=50)
    active = models.IntegerField()
    inActive = models.TextField()
    maxActive = models.TextField()
    count = models.IntegerField()
    errors = models.IntegerField()
    timeOuts = models.TextField()
    latency = models.IntegerField()
    peakLatency = models.IntegerField()
    throughPut = models.IntegerField()

    def __str__(self):
        return '<Client: {}>'.format(self.name)


class ClientParentRow(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    address = models.CharField(max_length=50)
    active = models.IntegerField()
    inActive = models.TextField()
    maxActive = models.TextField()
    count = models.IntegerField()
    errors = models.IntegerField()
    timeOuts = models.TextField()
    latency = models.IntegerField()
    peakLatency = models.IntegerField()
    throughPut = models.IntegerField()

    def __str__(self):
        return '<ClientParent: {}>'.format(self.name)


class ServerRow(models.Model):
    parentName = models.CharField(max_length=50)
    name = models.CharField(max_length=20, primary_key=True)
    address = models.CharField(max_length=50)
    active = models.IntegerField()
    maxActive = models.TextField()
    count = models.IntegerField()
    errors = models.IntegerField()
    latency = models.IntegerField()
    peakLatency = models.IntegerField()
    throughPut = models.IntegerField()

    def __str__(self):
        return '<Server: {}>'.format(self.name)


class AlarmRow(models.Model):
    name = models.CharField(max_length=40)
    module = models.CharField(max_length=25, primary_key=True)
    id = models.IntegerField()
    description = models.TextField()
    raised = models.IntegerField()
    lastRaised = models.TextField()
    cleared = models.IntegerField()
    lastCleared = models.CharField(max_length=30)

    def __str__(self):
        return '<Alarm: {}>'.format(self.name)


class CharsRow(models.Model):
    parentName = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    error = models.CharField(max_length=40)
    count = models.IntegerField()
    lastOccurence = models.TextField()

    def __str__(self):
        return '<Char: {}>'.format(self.name)

from django.db import models


class ClientRow(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    address = models.CharField(max_length=50)
    active = models.IntegerField()
    inActive = models.TextField()
    maxActive = models.TextField()
    count = models.IntegerField()
    errors = models.IntegerField()
    timeOuts = models.TextField()
    latency = models.CharField(max_length=20)
    peakLatency = models.CharField(max_length=20)
    throughPut = models.TextField()

    def __str__(self):
        return '<Name: {}>'.format(self.name)


class ServerRow(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    address = models.CharField(max_length=50)
    active = models.IntegerField()
    maxActive = models.TextField()
    count = models.IntegerField()
    errors = models.IntegerField()
    latency = models.CharField(max_length=20)
    peakLatency = models.CharField(max_length=20)
    throughPut = models.TextField()

    def __str__(self):
        return '<Name: {}>'.format(self.name)


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
        return '<Name: {}>'.format(self.name)

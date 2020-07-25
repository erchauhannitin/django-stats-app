from django.db import models


class ReportRow(models.Model):
    name = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    active = models.IntegerField()
    inActive = models.IntegerField()
    maxAactive = models.IntegerField()
    count = models.IntegerField()
    errors = models.IntegerField()
    timeOuts = models.IntegerField()
    latency = models.IntegerField()
    peakLatency = models.IntegerField()
    throughPut = models.TextField()

    def __str__(self):
        return '<Name: {}>'.format(self.name)

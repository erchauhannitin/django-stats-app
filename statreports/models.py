from django.db import models


class ReportRow(models.Model):
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

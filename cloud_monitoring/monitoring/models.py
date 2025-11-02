from django.db import models
import random

class Metric(models.Model):
    name = models.CharField(max_length=100)
    threshold = models.FloatField()

    def __str__(self):
        return self.name

from django.db import models
from django.utils import timezone
class MonitorLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    cpu_usage = models.FloatField()
    memory_usage = models.FloatField()
    disk_usage = models.FloatField()

    def __str__(self):
        return f"Log at {self.timestamp}"

class Alert(models.Model):
    monitor = models.ForeignKey(MonitorLog, on_delete=models.CASCADE)
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.monitor.name} = {self.value}"
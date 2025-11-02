from django.contrib import admin

# Register your models here.
from .models import Metric, MonitorLog, Alert
admin.site.register(Metric)
admin.site.register(MonitorLog)
admin.site.register(Alert)
import psutil
import time
from django.core.management.base import BaseCommand
from monitoring.models import MonitorLog, Metric, Alert
print("Starting the monitoring command...")
from django.conf import settings
import time

class Command(BaseCommand):
    help = 'Check and log system metrics, and generate alerts if thresholds are exceeded.'

    def handle(self, *args, **kwargs):
        while True:
            # Gather system metrics
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent

            # Save log
            log = MonitorLog.objects.create(
                cpu_usage=cpu,
                memory_usage=memory,
                disk_usage=disk
            )

            # Fetch metric thresholds
            thresholds = {m.name.lower(): m.threshold for m in Metric.objects.all()}

            # Check for alerts
            if 'cpu' in thresholds and cpu > thresholds['cpu']:
                Alert.objects.create(
                    metric_name="CPU",
                    monitor=log,
                    value=cpu,
                    threshold=thresholds['cpu']
                )

            if 'memory' in thresholds and memory > thresholds['memory']:
                Alert.objects.create(
                    metric_name="Memory",
                    monitor=log,
                    value=memory,
                    threshold=thresholds['memory']
                )

            if 'disk' in thresholds and disk > thresholds['disk']:
                Alert.objects.create(
                    metric_name="Disk",
                    monitor=log,
                    value=disk,
                    threshold=thresholds['disk']
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Logged: CPU={cpu}%, MEM={memory}%, DISK={disk}%"
                )
            )

            # Sleep for 5 minutes (300 seconds)
            time.sleep(10)
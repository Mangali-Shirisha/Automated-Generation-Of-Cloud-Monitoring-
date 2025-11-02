from celery import shared_task
from .models import Monitor, Alert
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import random

@shared_task
def check_metrics():
    monitors = Monitor.objects.filter(is_active=True)
    for monitor in monitors:
        value = random.uniform(0, 100)  # Replace with real API
        if value > monitor.metric.threshold:
            alert = Alert.objects.create(
                monitor=monitor,
                message=f"ALERT: {monitor.metric.name} = {value:.2f} (Threshold = {monitor.metric.threshold})"
            )
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                'alerts_group',
                {
                    'type': 'send_alert',
                    'message': alert.message,
                }
            )

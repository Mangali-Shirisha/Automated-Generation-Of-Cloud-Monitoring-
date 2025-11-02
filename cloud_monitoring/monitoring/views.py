from django.shortcuts import render
from monitoring.models import MonitorLog, Alert
import random
from datetime import datetime, timedelta

def dashboard(request):
    # Get recent alerts and logs
    alerts = Alert.objects.order_by('-timestamp')
    logs = MonitorLog.objects.order_by('-timestamp')# Get more logs for the table
    
    # Calculate overall statistics
    if logs.exists():
        avg_cpu = round(sum(log.cpu_usage for log in logs) / len(logs), 1)
        avg_memory = round(sum(log.memory_usage for log in logs) / len(logs), 1)
        avg_disk = round(sum(log.disk_usage for log in logs) / len(logs), 1)
        
        # Determine status based on thresholds
        def get_status(value, warning_thresh=70, critical_thresh=90):
            if value >= critical_thresh:
                return 'critical'
            elif value >= warning_thresh:
                return 'warning'
            return 'healthy'
        
        cpu_status = get_status(avg_cpu)
        memory_status = get_status(avg_memory)
        disk_status = get_status(avg_disk)
    else:
        avg_cpu = avg_memory = avg_disk = 0
        cpu_status = memory_status = disk_status = 'healthy'
    
    # Generate sample data for CPU cores and disk partitions
    cpu_cores = [
        {'core': 1, 'usage': random.randint(20, 80)},
        {'core': 2, 'usage': random.randint(20, 80)},
        {'core': 3, 'usage': random.randint(20, 80)},
        {'core': 4, 'usage': random.randint(20, 80)}
    ]
    
    disk_partitions = [
        {'mount': '/', 'total_gb': 100, 'used_gb': 45, 'percent': 45},
        {'mount': '/home', 'total_gb': 500, 'used_gb': 320, 'percent': 64},
        {'mount': '/var', 'total_gb': 200, 'used_gb': 80, 'percent': 40}
    ]
    
    # Network stats (sample data)
    network_in = round(random.uniform(10, 50), 1)
    
    context = {
        'logs': logs,
        'alerts': alerts,
        'overall_stats': {
            'avg_cpu': avg_cpu,
            'avg_memory': avg_memory,
            'avg_disk': avg_disk,
            'cpu_status': cpu_status,
            'memory_status': memory_status,
            'disk_status': disk_status,
            'network_in': network_in
        },
        'cpu_cores': cpu_cores,
        'disk_partitions': disk_partitions,
        
        # For the frontend charts (sample data - in production you'd generate this from your logs)
        'chart_data': {
            'timestamps': [
                (datetime.now() - timedelta(hours=i)).strftime('%H:%M') 
                for i in range(12, -1, -1)
            ],
            'cpu_data': [random.randint(20, 80) for _ in range(13)],
            'memory_data': [random.randint(30, 85) for _ in range(13)],
            'disk_data': [random.randint(40, 90) for _ in range(13)],
            'network_in_data': [random.randint(5, 50) for _ in range(13)],
            'network_out_data': [random.randint(2, 30) for _ in range(13)]
        }
    }
    
    return render(request, 'dashboard.html', context)
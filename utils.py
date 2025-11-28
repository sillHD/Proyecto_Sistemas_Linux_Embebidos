# utils.py
import psutil
import time

last_monitor_time = time.perf_counter()
monitor_interval = 0.5  # segundos

def gpu_usage():
    try:
        with open("/sys/class/drm/card0/device/gpu_busy_percent") as f:
            return int(f.read().strip())
    except:
        return 0

def monitor_usage():
    global last_monitor_time
    current_time = time.perf_counter()
    if current_time - last_monitor_time >= monitor_interval:
        cpu = psutil.cpu_percent(interval=0.0)
        gpu = gpu_usage()
        print(f"CPU: {cpu:.1f}% | GPU: {gpu}%")
        last_monitor_time = current_time

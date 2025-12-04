# utils.py  (para Juego_2)
import psutil
import time

# Tiempo del último muestreo
_last_monitor_time = time.perf_counter()
# Intervalo entre impresiones (segundos)
_MONITOR_INTERVAL = 0.5

def gpu_usage():
    """Devuelve porcentaje de GPU o 0 si no está disponible."""
    try:
        with open("/sys/class/drm/card0/device/gpu_busy_percent") as f:
            return int(f.read().strip())
    except Exception:
        return 0

def monitor_usage():
    """Imprime uso de CPU/GPU cada _MONITOR_INTERVAL segundos."""
    global _last_monitor_time
    now = time.perf_counter()
    if now - _last_monitor_time >= _MONITOR_INTERVAL:
        cpu = psutil.cpu_percent(interval=0.0)
        gpu = gpu_usage()
        print(f"CPU: {cpu:.1f}% | GPU: {gpu}%")
        _last_monitor_time = now

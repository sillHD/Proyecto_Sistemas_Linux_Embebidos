#!/usr/bin/env python3
# measure_beagle.py
# Script para medir rendimiento en BeaglePlay y generar reporte

import os
import sys
import subprocess
import json
from datetime import datetime

def run_command(cmd):
    """Ejecuta comando y retorna output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except Exception as e:
        return f"ERROR: {e}"

def get_system_info():
    """Obtiene información del sistema."""
    info = {}
    
    # CPU
    info['cpu_cores'] = run_command("nproc").strip()
    info['cpu_model'] = run_command("cat /proc/cpuinfo | grep 'model name' | head -1").strip()
    
    # GPU
    info['gpu'] = run_command("glxinfo | grep 'Device:' | head -1").strip()
    info['opengl_version'] = run_command("glxinfo | grep 'OpenGL version' | head -1").strip()
    
    # Memoria
    info['ram_total'] = run_command("free -h | grep Mem | awk '{print $2}'").strip()
    info['ram_available'] = run_command("free -h | grep Mem | awk '{print $7}'").strip()
    
    # OS
    info['os'] = run_command("cat /etc/os-release | grep PRETTY_NAME").strip()
    
    return info

def measure_game_performance(duration=30):
    """Ejecuta el juego y mide rendimiento."""
    print(f"\n[*] Ejecutando juego por {duration} segundos...")
    
    # Iniciar juego en background
    import time
    process = subprocess.Popen([sys.executable, "main_opl.py"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
    
    # Dar tiempo para que cargue
    time.sleep(3)
    
    # Medir recursos durante ejecución
    measurements = []
    for i in range(duration // 2):
        time.sleep(2)
        try:
            # Obtener PID del proceso
            pid = process.pid
            
            # CPU y memoria
            stat = run_command(f"cat /proc/{pid}/stat").split()
            mem = run_command(f"cat /proc/{pid}/status | grep VmRSS").split()[-2]
            
            measurements.append({
                'timestamp': i * 2,
                'memory_kb': int(mem) if mem.isdigit() else 0,
                'cpu_time': float(stat[13]) + float(stat[14]) if len(stat) > 14 else 0,
            })
        except:
            pass
    
    # Terminar juego
    process.terminate()
    
    return measurements

def main():
    print("=" * 70)
    print("MEDIDOR DE RENDIMIENTO - BeaglePlay")
    print("=" * 70)
    
    timestamp = datetime.now().isoformat()
    
    # Recopilar información
    print("\n[*] Obteniendo información del sistema...")
    sys_info = get_system_info()
    
    print("\n[*] Información del Sistema:")
    for key, value in sys_info.items():
        print(f"  {key}: {value}")
    
    # Medir rendimiento
    measurements = measure_game_performance(duration=30)
    
    print(f"\n[*] Se tomaron {len(measurements)} mediciones.")
    
    if measurements:
        avg_mem = sum(m['memory_kb'] for m in measurements) / len(measurements)
        max_mem = max(m['memory_kb'] for m in measurements)
        print(f"  Memoria promedio: {avg_mem:.0f} KB ({avg_mem/1024:.1f} MB)")
        print(f"  Memoria máxima: {max_mem:.0f} KB ({max_mem/1024:.1f} MB)")
    
    # Generar reporte JSON
    report = {
        'timestamp': timestamp,
        'system_info': sys_info,
        'measurements': measurements,
        'summary': {
            'total_measurements': len(measurements),
            'avg_memory_mb': (avg_mem / 1024) if measurements else 0,
            'max_memory_mb': (max_mem / 1024) if measurements else 0,
        }
    }
    
    # Guardar reporte
    report_file = f"beagle_report_{timestamp.replace(':', '-').split('.')[0]}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n[✓] Reporte guardado: {report_file}")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()

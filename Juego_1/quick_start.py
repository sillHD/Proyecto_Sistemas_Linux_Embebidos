#!/usr/bin/env python3
# quick_start.py
# Script para generar el atlas y ejecutar el juego con mediciones

import subprocess
import os
import sys

def main():
    print("=" * 70)
    print("JUEGO OPENGL OPTIMIZADO - INICIO RÁPIDO")
    print("=" * 70)
    
    # Opción 1: Generar atlas
    print("\n[1/3] ¿Generar texture atlas? (s/n)")
    if input().strip().lower() == 's':
        print("Generando atlas...")
        try:
            subprocess.run([sys.executable, "texture_atlas_generator.py"], check=True)
            print("✓ Atlas generado.")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Opción 2: ¿Profiling?
    print("\n[2/3] ¿Activar profiling con cProfile? (s/n)")
    profiling_enabled = input().strip().lower() == 's'
    
    # Opción 3: Ejecutar juego
    print("\n[3/3] Ejecutando juego...")
    print("Controles:")
    print("  - FLECHA DERECHA: Mover derecha")
    print("  - FLECHA IZQUIERDA: Mover izquierda")
    print("  - FLECHA ARRIBA: Saltar")
    print("  - ESC: Salir")
    print("\nTiempo de respuesta (FPS) se mostrará cada 5 segundos.\n")
    
    if profiling_enabled:
        print("⚠ Profiling activado (más lento). Guarde en perfil.pstats al salir.")
    
    # Ejecutar el juego
    try:
        if profiling_enabled:
            # Activar profiling mediante variable de entorno
            env = os.environ.copy()
            env['ENABLE_PROFILING'] = '1'
            subprocess.run([sys.executable, "main_opl.py"], env=env)
        else:
            subprocess.run([sys.executable, "main_opl.py"])
    except KeyboardInterrupt:
        print("\n✓ Juego cerrado.")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 70)
    print("Para más información, ver OPTIMIZATION_README.md")
    print("=" * 70)

if __name__ == "__main__":
    main()

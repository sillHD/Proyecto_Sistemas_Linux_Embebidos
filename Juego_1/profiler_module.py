# profiler_module.py
# Módulo para medir FPS en tiempo real y generar perfiles con cProfile

import time
import cProfile
import pstats
import io
from contextlib import contextmanager

class FPSCounter:
    """Contador de FPS en tiempo real."""
    
    def __init__(self, window_size=60):
        self.window_size = window_size
        self.frame_times = []
        self.last_time = time.perf_counter()
    
    def tick(self):
        """Llamar una vez por frame."""
        current_time = time.perf_counter()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        self.frame_times.append(dt)
        if len(self.frame_times) > self.window_size:
            self.frame_times.pop(0)
    
    def get_fps(self):
        """Retorna FPS promedio de los últimos N frames."""
        if not self.frame_times:
            return 0.0
        avg_dt = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg_dt if avg_dt > 0 else 0.0
    
    def get_ms_per_frame(self):
        """Retorna ms promedio por frame."""
        if not self.frame_times:
            return 0.0
        return (sum(self.frame_times) / len(self.frame_times)) * 1000.0


class GameProfiler:
    """Profiler para medir rendimiento del juego con cProfile."""
    
    def __init__(self, output_file="perfil.pstats"):
        self.profiler = cProfile.Profile()
        self.output_file = output_file
        self.running = False
    
    def start(self):
        """Inicia la profiling."""
        self.profiler.enable()
        self.running = True
        print(f"Profiling iniciado... (guardará en {self.output_file})")
    
    def stop(self):
        """Detiene la profiling y guarda resultados."""
        if self.running:
            self.profiler.disable()
            self.profiler.dump_stats(self.output_file)
            self.running = False
            print(f"Profiling guardado: {self.output_file}")
            self.print_stats()
    
    def print_stats(self, top_n=20):
        """Imprime top N funciones más lentas."""
        s = io.StringIO()
        ps = pstats.Stats(self.profiler, stream=s).sort_stats('cumulative')
        ps.print_stats(top_n)
        print("\n=== TOP FUNCIONES MÁS LENTAS ===")
        print(s.getvalue())


@contextmanager
def profile_section(name):
    """Context manager para medir tiempo de una sección de código."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"[{name}] {elapsed:.2f} ms")


# Utilidades para medir draw calls
class DrawCallCounter:
    """Cuenta draw calls por frame."""
    
    def __init__(self):
        self.draw_calls = 0
        self.texture_binds = 0
    
    def reset(self):
        self.draw_calls = 0
        self.texture_binds = 0
    
    def record_draw_call(self):
        self.draw_calls += 1
    
    def record_texture_bind(self):
        self.texture_binds += 1
    
    def report(self):
        return f"Draw calls: {self.draw_calls}, Texture binds: {self.texture_binds}"

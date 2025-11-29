# Optimizaciones del Juego OpenGL - Guía de Uso

## Cambios Realizados

### 1. **Renderer Moderno (VBO/VAO + Shaders)**
- **Archivo**: `renderer_vbo.py`
- Implementación preparada de un renderer moderno con VBO/VAO y shaders GLSL ES 3.0.
- Reduce drásticamente draw calls y binds de texturas.
- Aunque está preparado, el juego actualmente usa batching ligero por compatibilidad.

### 2. **Batching Ligero de Texturas**
- **Cambios en**: `funciones.py` y `main_opl.py`
- Los dibujados se encolan por `tex_id` en cada frame.
- Antes de renderizar, se agrupa: `for tex_id, quads in draw_queue.items(): draw_batch(tex_id, quads)`
- Reduce `glBindTexture` de ~15-20 por frame a ~5-8.

### 3. **Mipmaps Automáticos**
- **Cambios en**: `funciones.load_texture_from_surface()`
- Genera automáticamente mipmaps al cargar texturas.
- Usa `GL_LINEAR_MIPMAP_LINEAR` para mejor calidad y rendimiento en escalado.
- Wrap mode: `GL_CLAMP_TO_EDGE`.

### 4. **Medición de FPS en Tiempo Real**
- **Archivo**: `profiler_module.py`
- `FPSCounter`: Mide FPS e ms/frame cada 5 segundos.
- Salida en consola (aprox. cada 300 frames @ 60 FPS).

### 5. **Profiling con cProfile**
- **Archivo**: `profiler_module.py`
- `GameProfiler`: Genera `perfil.pstats` con datos de profiling.
- Usa: `python -m pstats perfil.pstats` para analizar.

### 6. **Generador de Texture Atlas**
- **Archivo**: `texture_atlas_generator.py`
- Empaqueta sprites en una sola textura (PNG) + metadatos (JSON con UVs).
- Uso:
  ```bash
  python texture_atlas_generator.py
  ```
- Genera: `atlas.png` y `atlas.json`.
- *Nota: Opcional para ahora; es paso intermedio hacia instancing.*

---

## Cómo Ejecutar el Juego (Versión Optimizada)

### PowerShell (Windows):
```powershell
cd 'C:\Users\ismae\Desktop\Semestre_actual\Estructuras_Computacionales\Proyecto_Sistemas_Linux_Embebidos\Juego_1'
python main_opl.py
```

### Esperado:
- Juego ejecutándose normalmente.
- Cada 5 segundos, verás en consola: `FPS: XX.X | MS/Frame: X.XX`
- Si todo está bien, deberías ver FPS cercano a 60 (o lo que soporte tu GPU).

---

## Medir Rendimiento

### 1. **FPS en Tiempo Real** (ya integrado)
El juego imprime automáticamente cada 5 segundos.

### 2. **Profiling Completo con cProfile**
1. En `main_opl.py`, línea ~164, descomenta:
   ```python
   # profiler.start()  <- DESCOMENTAR
   ```
2. Ejecuta el juego, juega unos segundos y cierra (ESC).
3. Se generará `perfil.pstats`.
4. Analiza:
   ```powershell
   python -m pstats perfil.pstats
   (pstats) sort cumulative
   (pstats) stats 20  # Top 20 funciones
   (pstats) quit
   ```

### 3. **Medir en BeaglePlay**
```bash
# SSH a BeaglePlay
ssh root@192.168.x.x

# Ir a la carpeta del juego
cd /path/to/Juego_1

# Ejecutar con profiling
python main_opl.py

# En otra terminal SSH, ver recursos en tiempo real
top -p $(pgrep python)
# O más detallado:
perf record -p $(pgrep python) -g
```

---

## Próximos Pasos de Optimización (Prioridad)

### 1. **Implementar Renderer VBO/VAO Completo** (Mayor impacto)
- Usar `BatchRenderer` de `renderer_vbo.py`.
- Crear un texture atlas (sprite sheets).
- Renderizar con `glDrawElements` o `glDrawElementsInstanced`.
- **Ganancia esperada**: 50-80% más rápido en GPU.

### 2. **Crear Texture Atlas**
- Usar `texture_atlas_generator.py` para empaquetar todos los sprites.
- Cargar metadatos y usar UVs normalizadas.
- Reduce memoria y ancho de banda de texturas.
- **Ganancia esperada**: 30-50% menos memoria VRAM.

### 3. **Compresión ETC2**
- Convertir atlas a texturas comprimidas (ETC2) para producción en BeaglePlay.
- Herramientas: `etcpack`, `PVRTexToolCLI`, `astcenc`.
- **Ganancia esperada**: 4-6x menor tamaño de texturas en VRAM.

### 4. **Reducir Resoluciones de Texturas**
- Analizar con `perfil.pstats` qué consume más.
- Muchas texturas no necesitan 4K; 512x512 o 1024x1024 puede ser suficiente.

### 5. **Portabilidad a C++/SDL2** (Si aún hace falta)
- Python + pygame puede ser un cuello de botella en sistemas embebidos.
- Considerar portar renderer crítico a C++ con SDL2 + OpenGL ES 3.1.

---

## Estructura de Archivos

```
Juego_1/
├── main_opl.py                 # Juego principal (con FPS + profiling)
├── funciones.py                # Funciones OpenGL (batching + mipmaps)
├── settings.py                 # Configuración
├── renderer_vbo.py             # Renderer VBO/VAO (opcional, preparado)
├── profiler_module.py          # FPSCounter, GameProfiler
├── texture_atlas_generator.py  # Generador de texture atlas
├── texturas/                   # Sprites individuales
└── ... (resto de archivos)
```

---

## Notas Técnicas

- **Batching ligero actual**: Agrupa por `tex_id`, reduce glBindTexture pero sigue usando `glBegin/glEnd`.
- **VBO/VAO renderer**: Preparado en `renderer_vbo.py`, requiere adaptación de `main_opl.py` para usarlo.
- **OpenGL ES 3.1**: BeaglePlay soporta; `glGenerateMipmap`, `GL_LINEAR_MIPMAP_LINEAR` están disponibles.
- **Profiling**: `cProfile` mide CPU; para GPU, usa herramientas como `perf` o `glxinfo` en BeaglePlay.

---

## Troubleshooting

### "renderer_vbo not available"
- Normal si no necesitas VBO aún. Sistema sigue funcionando con batching ligero.

### "profiler_module not available"
- Opcional. Juego ejecuta sin profiling; desactiva si causa problemas.

### FPS bajo en BeaglePlay
1. Verifica con `top` si CPU o GPU es cuello de botella.
2. Si CPU (Python): considera portar a C++.
3. Si GPU: revisa resoluciones de texturas, reduce draw calls con atlas.
4. Si memoria: activa compresión ETC2.

---

**Versión**: 1.0  
**Fecha**: 29 de noviembre de 2025  
**Estado**: Optimizado con batching ligero + mipmaps + FPS tracking.

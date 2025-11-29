# texture_atlas_generator.py
# Genera un atlas de texturas a partir de archivos PNG en un directorio
# Salida: atlas.png + atlas.json (con UVs para cada sprite)

import os
import json
from PIL import Image
import glob

def generate_atlas(source_dirs, output_dir, atlas_name="atlas", max_width=2048, max_height=2048):
    """
    Genera un texture atlas a partir de directorios de sprites.
    
    Args:
        source_dirs: lista de directorios o patrones glob (ej. ["texturas/walk/right/*.png", ...])
        output_dir: directorio donde guardar atlas.png y atlas.json
        atlas_name: nombre base del atlas
        max_width, max_height: dimensiones máximas del atlas
    
    Returns:
        Ruta al PNG del atlas y ruta al JSON con UVs
    """
    
    # Recopilar todas las imágenes
    images = {}
    for pattern in source_dirs:
        for filepath in glob.glob(pattern):
            if os.path.isfile(filepath):
                try:
                    img = Image.open(filepath).convert("RGBA")
                    name = os.path.splitext(os.path.basename(filepath))[0]
                    images[name] = img
                except Exception as e:
                    print(f"Error cargando {filepath}: {e}")
    
    if not images:
        print("No se encontraron imágenes para el atlas.")
        return None, None
    
    print(f"Empaquetando {len(images)} imágenes en atlas...")
    
    # Empaquetar sprites (algoritmo simple: fila por fila)
    sorted_names = sorted(images.keys(), key=lambda k: images[k].size[0] * images[k].size[1], reverse=True)
    
    atlas_data = {}
    current_x, current_y = 0, 0
    max_row_height = 0
    
    # Crear canvas
    atlas = Image.new("RGBA", (max_width, max_height), (0, 0, 0, 0))
    
    for name in sorted_names:
        img = images[name]
        w, h = img.size
        
        # Si no cabe en la fila actual, pasar a la siguiente
        if current_x + w > max_width:
            current_x = 0
            current_y += max_row_height
            max_row_height = 0
        
        # Si no cabe en altura, error
        if current_y + h > max_height:
            print(f"Advertencia: No cabe todo el atlas. Cortando...")
            break
        
        # Pegar imagen en atlas
        atlas.paste(img, (current_x, current_y), img)
        
        # Guardar UVs (normalizado 0..1)
        atlas_data[name] = {
            "x": current_x,
            "y": current_y,
            "w": w,
            "h": h,
            "u0": current_x / max_width,
            "v0": current_y / max_height,
            "u1": (current_x + w) / max_width,
            "v1": (current_y + h) / max_height,
        }
        
        current_x += w
        max_row_height = max(max_row_height, h)
    
    # Recortar canvas al tamaño real usado
    actual_width = max_width
    actual_height = current_y + max_row_height
    atlas = atlas.crop((0, 0, actual_width, actual_height))
    
    # Guardar atlas
    os.makedirs(output_dir, exist_ok=True)
    atlas_png = os.path.join(output_dir, f"{atlas_name}.png")
    atlas_json = os.path.join(output_dir, f"{atlas_name}.json")
    
    atlas.save(atlas_png, "PNG")
    print(f"Atlas guardado: {atlas_png} ({actual_width}x{actual_height})")
    
    # Guardar metadatos
    metadata = {
        "width": actual_width,
        "height": actual_height,
        "sprites": atlas_data,
    }
    
    with open(atlas_json, "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadatos guardados: {atlas_json}")
    
    return atlas_png, atlas_json


def load_atlas(json_path):
    """Carga metadatos del atlas desde JSON."""
    with open(json_path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    # Ejemplo de uso
    source_patterns = [
        "texturas/walk/right/*.png",
        "texturas/walk/left/*.png",
        "texturas/jump/jump_right/*.png",
        "texturas/jump/jump_left/*.png",
        "texturas/enemy/right/*.png",
        "texturas/enemy/left/*.png",
        "texturas/clouds/*.png",
    ]
    
    generate_atlas(source_patterns, ".", atlas_name="sprites_atlas")

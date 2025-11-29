# renderer_vbo.py
# Renderer moderno con VBO/VAO + shaders para OpenGL ES 3.0+
# Reduce draw calls y binds drásticamente vs immediate mode

import numpy as np
from OpenGL.GL import *
import math
import ctypes

# ============================================================
# SHADERS
# ============================================================

VERTEX_SHADER = """
#version 300 es
precision highp float;

layout(location=0) in vec2 a_position;
layout(location=1) in vec2 a_texcoord;

uniform mat4 u_projection;

out vec2 v_texcoord;

void main() {
    gl_Position = u_projection * vec4(a_position, 0.0, 1.0);
    v_texcoord = a_texcoord;
}
"""

FRAGMENT_SHADER = """
#version 300 es
precision mediump float;

in vec2 v_texcoord;
uniform sampler2D u_texture;

out vec4 o_color;

void main() {
    o_color = texture(u_texture, v_texcoord);
}
"""

# ============================================================
# COMPILACIÓN DE SHADERS
# ============================================================

def compile_shader(source, shader_type):
    """Compila un shader individual."""
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        print(f"Shader compilation error ({shader_type}): {error}")
        raise RuntimeError(f"Shader compilation failed: {error}")
    
    return shader

def create_program():
    """Crea el programa OpenGL con vertex y fragment shader."""
    vertex = compile_shader(VERTEX_SHADER, GL_VERTEX_SHADER)
    fragment = compile_shader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    
    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)
    
    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        print(f"Program linking error: {error}")
        raise RuntimeError(f"Program linking failed: {error}")
    
    glDeleteShader(vertex)
    glDeleteShader(fragment)
    
    return program

# ============================================================
# BATCH RENDERER
# ============================================================

class BatchRenderer:
    """Renderer que agrupa quads por textura y los dibuja con VBO/VAO."""
    
    def __init__(self, max_quads_per_batch=10000):
        self.max_quads = max_quads_per_batch
        self.program = create_program()
        
        # Ubicaciones de atributos
        self.u_projection = glGetUniformLocation(self.program, "u_projection")
        self.u_texture = glGetUniformLocation(self.program, "u_texture")
        
        # Crear VAO y VBO
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        
        # Alocar espacio para vertices (4 verts por quad * max_quads * 4 floats por vert)
        buffer_size = self.max_quads * 4 * 4 * 4  # 4 verts, 4 floats (pos.xy + uv.xy)
        glBufferData(GL_ARRAY_BUFFER, buffer_size, None, GL_DYNAMIC_DRAW)
        
        # Configurar atributos: posición (2 floats) + texcoord (2 floats)
        glEnableVertexAttribArray(0)  # position
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(1)  # texcoord
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))
        
        # Crear IBO (índices para dibujar quads como triangles)
        self.ibo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ibo)
        
        indices = []
        for i in range(self.max_quads):
            base = i * 4
            indices.extend([base, base+1, base+2, base+2, base+3, base])
        
        indices = np.array(indices, dtype=np.uint32)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
        
        self.index_count = len(indices)
        self.batches = {}  # {tex_id: [list of quads]}
    
    def add_quad(self, tex_id, x, y, w, h, u0=0.0, v0=0.0, u1=1.0, v1=1.0):
        """Añade un quad a la cola para una textura específica."""
        if tex_id not in self.batches:
            self.batches[tex_id] = []
        
        # Quad como 4 vértices (pos.xy, uv.xy)
        quad = np.array([
            x,     y,     u0, v0,
            x + w, y,     u1, v0,
            x + w, y + h, u1, v1,
            x,     y + h, u0, v1,
        ], dtype=np.float32)
        
        self.batches[tex_id].append(quad)
    
    def flush(self, projection_matrix):
        """Dibuja todos los quads encolados, agrupa por textura."""
        if not self.batches:
            return
        
        glUseProgram(self.program)
        glUniformMatrix4fv(self.u_projection, 1, GL_TRUE, projection_matrix)
        glUniform1i(self.u_texture, 0)
        
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        
        offset = 0
        for tex_id, quads in self.batches.items():
            if not quads:
                continue
            
            # Convertir lista de quads a array
            vertex_data = np.vstack(quads)
            quad_count = len(quads)
            
            # Subir datos al VBO
            glBufferSubData(GL_ARRAY_BUFFER, offset * 16, vertex_data.nbytes, vertex_data)
            
            # Dibujar
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glDrawElements(GL_TRIANGLES, quad_count * 6, GL_UNSIGNED_INT, 
                          ctypes.c_void_p(offset * 6 * 4))
            
            offset += quad_count * 4
        
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glUseProgram(0)
        
        # Limpiar batches para el próximo frame
        self.batches = {}
    
    def clear(self):
        """Limpia los batches sin dibujar."""
        self.batches = {}


# ============================================================
# ORTHO MATRIX (para 2D)
# ============================================================

def ortho(left, right, bottom, top, near, far):
    """Crea una matriz de proyección ortho (2D)."""
    result = np.zeros((4, 4), dtype=np.float32)
    
    result[0, 0] = 2.0 / (right - left)
    result[1, 1] = 2.0 / (top - bottom)
    result[2, 2] = -2.0 / (far - near)
    result[3, 3] = 1.0
    
    result[0, 3] = -(right + left) / (right - left)
    result[1, 3] = -(top + bottom) / (top - bottom)
    result[2, 3] = -(far + near) / (far - near)
    
    return result

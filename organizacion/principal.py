from cmath import cos, pi, sin
from OpenGL.GL import *
from Asteroide import Asteroide
from glew_wish import *
import glfw
import math
from Nave import *
import random

window = None
tiempo_anterior = 0.0

nave = Nave()
asteroides = []

def actualizar():
    global tiempo_anterior
    global window

    tiempo_actual = glfw.get_time()
    # Cuanto tiempo paso entre la ejecucion actual
    # y la inmediata anterior de esta funcion
    tiempo_delta = tiempo_actual - tiempo_anterior

    nave.actualizar(window, tiempo_delta)
    for asteroide in asteroides:
        if asteroide.vivo:
            asteroide.actualizar(tiempo_delta)
            if asteroide.colisionando(nave):
                nave.herido = True
            for bala in nave.balas:
                if bala.disparando:
                    if asteroide.colisionando(bala):
                        bala.disparando = False
                        asteroide.vivo = False  
    tiempo_anterior = tiempo_actual
    
def colisionando():
    colisionando = False
    # Método de Bounding box:
    # Extremo derecho del triangulo >= Extremo izquierdo cuadrado
    # Extremo izquierdo del triangulo <= Extremo derecho cuadrado
    # Extremo superior del triangulo >= Extremo inferior del cuadrado
    # Extremo inferior del triangulo <= Extremo superior del cuadrado

    return colisionando

def draw():
    nave.dibujar()
    for asteroide in asteroides:
        asteroide.dibujar()

def inicializar_asteroides():
    for i in range(10):
        posicion_x = (random.random() * 2) - 1
        posicion_y = (random.random() * 2) - 1
        direccion = random.random() * 360
        velocidad = (random.random() * 0.5)
        asteroides.append(Asteroide(posicion_x, posicion_y, 
            direccion, velocidad))

def main():
    global window

    width = 700
    height = 700
    # Inicializar GLFW
    if not glfw.init():
        return

    #declarar ventana
    window = glfw.create_window(width, height, "Mi ventana", None, None)

    # Configuraciones de OpenGL
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    # Verificamos la creacion de la ventana
    if not window:
        glfw.terminate()
        return

    # Establecer el contexto
    glfw.make_context_current(window)

    # Le dice a GLEW que si usaremos el GPU
    glewExperimental = True

    # Inicializar glew
    if glewInit() != GLEW_OK:
        print("No se pudo inicializar GLEW")
        return

    # Imprimir version
    version = glGetString(GL_VERSION)
    print(version)

    inicializar_asteroides()

    # Draw loop
    while not glfw.window_should_close(window):
        # Establecer el viewport
        # glViewport(0,0,width,height)
        # Establecer color de borrado
        glClearColor(0.7,0.7,0.7,1)
        # Borrar el contenido del viewport
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        actualizar()
        # Dibujar
        draw()

        # Polling de inputs
        glfw.poll_events()

        # Cambia los buffers
        glfw.swap_buffers(window)

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
#Comandos para librerías
#pip install pyopengl
#pip install glfw

#Importar librerias

from cmath import cos, pi, sin
from OpenGL.GL import *
from Asteroide import Asteroide
from glew_wish import *
import glfw
import math
from Nave import *

#unidades por segundo
window = None

#Bala
posiciones_bala = [
                [0.0,0.0,0.0],
                [0.0,0.0,0.0],
                [0.0,0.0,0.0]
                ]
disparando = [False,False,False]
angulo_bala = [0.0, 0.0, 0.0]
velocidad_bala = 0.75

tiempo_anterior = 0.0

estado_anterior_espacio = glfw.RELEASE

asteroide = Asteroide()
nave = Nave()

def actualizar_bala(tiempo_delta):
    global disparando
    for i in range(3):
        if disparando[i]:
            cantidad_movimiento = velocidad_bala * tiempo_delta
            posiciones_bala[i][0] = posiciones_bala[i][0] + (
                math.cos(angulo_bala[i] * pi / 180.0) * cantidad_movimiento
            )
            posiciones_bala[i][1] = posiciones_bala[i][1] + (
                math.sin(angulo_bala[i] * pi / 180.0) * cantidad_movimiento
            )
            #checar si está chocando contra enemigos
            #(Eso hay que hacerlo, no está hecho)

            #Checar si se salió de los límites:
            if (posiciones_bala[i][0] > 1 or posiciones_bala[i][0] < -1 or 
                posiciones_bala[i][1] > 1 or posiciones_bala[i][1] < -1):
                disparando[i] = False



def actualizar():
    global tiempo_anterior
    global window

    tiempo_actual = glfw.get_time()
    #Cuanto tiempo paso entre la ejecucion actual
    #y la inmediata anterior de esta funcion
    tiempo_delta = tiempo_actual - tiempo_anterior

    nave.actualizar_tirangulo(window, tiempo_delta)
    asteroide.actualizar(tiempo_delta)
    actualizar_bala(tiempo_delta)
    
    tiempo_anterior = tiempo_actual
    
def colisionando():
    colisionando = False
    #Método de bounding box:
    #Extrema derecha del triangulo >= Extrema izquierda cuadrado
    #Extrema izquierda del triangulo <= Extrema derecha cuadrado
    #Extremo superior del triangulo >= Extremo inferior del cuadrado
    #Extremo inferior del triangulo <= Extremo superior del cuadrado
    # if (nave.posicion_x + 0.05 >= nave.posicion_x - 0.05 
    #     and nave.posicion_x - 0.05 <= nave.posicion_x + 0.05 
    #     and nave.posicion_y + 0.05 >= nave.posicion_y - 0.05 
    #     and nave.posicion_y - 0.05 <= nave.posicion_y + 0.05):
        
    #     colisionando = True 
    return colisionando

def draw_bala():
    global posiciones_bala
    global disparando
    for i in range(3):
        if disparando[i]:
            glPushMatrix()
            glTranslatef(posiciones_bala[i][0], posiciones_bala[i][1], 0.0)
            glBegin(GL_QUADS)
            glColor3f(0.0, 0.0, 0.0)
            glVertex3f(-0.01,0.01,0.0)
            glVertex3f(0.01,0.01,0.0)
            glVertex3f(0.01,-0.01,0.0)
            glVertex3f(-0.01,-0.01,0.0)
            glEnd()
            glPopMatrix()

def draw():
    nave.dibujar()
    asteroide.dibujar()
    draw_bala()


def main():
    global window

    width = 700
    height = 700
    #Inicializar GLFW
    if not glfw.init():
        return

    #declarar ventana
    window = glfw.create_window(width, height, "Mi ventana", None, None)

    #Configuraciones de OpenGL
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    #Verificamos la creacion de la ventana
    if not window:
        glfw.terminate()
        return

    #Establecer el contexto
    glfw.make_context_current(window)

    #Le dice a GLEW que si usaremos el GPU
    glewExperimental = True

    #Inicializar glew
    if glewInit() != GLEW_OK:
        print("No se pudo inicializar GLEW")
        return

    #imprimir version
    version = glGetString(GL_VERSION)
    print(version)

    #Draw loop
    while not glfw.window_should_close(window):
        #Establecer el viewport
        #glViewport(0,0,width,height)
        #Establecer color de borrado
        glClearColor(0.7,0.7,0.7,1)
        #Borrar el contenido del viewport
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


        actualizar()
        #Dibujar
        draw()


        #Polling de inputs
        glfw.poll_events()

        #Cambia los buffers
        glfw.swap_buffers(window)

    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
from OpenGL.GL import *
from glew_wish import *
import glfw
import math

class Nave:
    posicion_x = 0.0
    posicion_y = 0.0
    posicion_z = 0.0

    velocidad = 0.5
    angulo = 0.0
    fase = 90.0
    velocidad_rotacion = 90.0

    estado_anterior_espacio = glfw.RELEASE

    def dibujar(self):
        
        glPushMatrix()

        glTranslatef(self.posicion_x, self.posicion_y, self.posicion_z)
        glRotatef(self.angulo, 0.0, 0.0, 1.0)
        glBegin(GL_TRIANGLES)

        glColor(0.0, 0.0, 0.0)

        #Manda vertices a dibujar
        glVertex3f(-0.05,-0.05,0)
        glVertex3f(0.0,0.05,0)
        glVertex3f(0.05,-0.05,0)
        glEnd()

        glPopMatrix()

    def actualizar_tirangulo(self, window, tiempo_delta):

        estado_tecla_arriba = glfw.get_key(window, glfw.KEY_UP)
        estado_tecla_derecha = glfw.get_key(window, glfw.KEY_RIGHT)
        estado_tecla_izquierda = glfw.get_key(window, glfw.KEY_LEFT)
        # estado_tecla_espacio = glfw.get_key(window, glfw.KEY_SPACE)

    # if (estado_tecla_espacio == glfw.PRESS and 
    #     estado_anterior_espacio == glfw.RELEASE):
    #     for i in range(3):
    #         if not disparando[i]:
    #             disparando[i] = True
    #             posiciones_bala[i][0] = self.posicion_x
    #             posiciones_bala[i][1] = self.posicion_y
    #             angulo_bala[i] = self.angulo + self.fase
    #             break

        cantidad_movimiento = self.velocidad * tiempo_delta
        if estado_tecla_arriba == glfw.PRESS:
            self.posicion_x = self.posicion_x + (
                math.cos((self.angulo + self.fase) * math.pi / 180.0) * cantidad_movimiento
            )
            self.posicion_y = self.posicion_y + (
                math.sin((self.angulo + self.fase) * math.pi / 180.0) * cantidad_movimiento
            )

        cantidad_rotacion = self.velocidad_rotacion * tiempo_delta
        if estado_tecla_izquierda == glfw.PRESS:
            self.angulo = self.angulo + cantidad_rotacion
            if self.angulo > 360.0:
                self.angulo = self.angulo - 360.0 
        if estado_tecla_derecha == glfw.PRESS:
            self.angulo = self.angulo - cantidad_rotacion
            if self.angulo < 0.0:
                self.angulo = self.angulo + 360.0
        
        if self.posicion_x > 1.05:
            self.posicion_x = -1.0
        if self.posicion_x < -1.05:
            self.posicion_x = 1.0

        if self.posicion_y > 1.05:
            self.posicion_y = -1.0
        if self.posicion_y < -1.05:
            self.posicion_y = 1.0

        # self.estado_anterior_espacio = estado_tecla_espacio
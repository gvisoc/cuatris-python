#-*- coding: utf-8 -*-
import pygame
import random

class Pieza:
    'Modela una pieza de Cuatris :)'
    def __init__(self, matriz, pantalla, lado_cuadrado):
        self.matriz = matriz
        # self.color = color
        # self.fondo = fondo
        self.pantalla = pantalla
        self.lado_cuadrado = lado_cuadrado
        # posición de la pieza
        self.x = 0
        self.y = 0
        self.calcula_dimensiones()

    def calcula_dimensiones(self):
        self.filas = len(self.matriz)
        self.columnas = len(self.matriz[0])

    def rotar90(self):
        'Rota la pieza en el sentido horario'
        self.matriz = list(zip(*self.matriz[::-1]))
        self.calcula_dimensiones()

    def rotarM90(self):
        'Rota la pieza en el sentido antihorario'
        self.matriz = list(zip(*self.matriz))[::-1]
        self.calcula_dimensiones()

    def __pinta_cuadrado(self, x, y, color):
        'dibuja un cuadrado en las coordenadas de malla especificadas'
        cuadrado = (x*self.lado_cuadrado,
                    y*self.lado_cuadrado,
                    self.lado_cuadrado,
                    self.lado_cuadrado)
        cuadrado_interno = (x*self.lado_cuadrado+8,
                            y*self.lado_cuadrado+8,
                            self.lado_cuadrado-16,
                            self.lado_cuadrado-16)
        pygame.draw.rect(self.pantalla,
                         (int(color[0]/2),
                          int(color[1]/2),
                          int(color[2]/2)),
                         cuadrado,
                         0)
        pygame.draw.rect(self.pantalla, color, cuadrado_interno, 0)

    def __borra_rectangulo(self, rectangulo):
        'borra el área especificada'
        pygame.draw.rect(self.pantalla, Cuatris.colores[0], rectangulo, 0)

    def pinta(self, x_ini, y_ini):
        'pinta la pieza especificada a partir de las coordenadas de malla x_ini, y_ini'
        # actualizamos la posición de la pieza
        self.x = x_ini
        self.y = y_ini
        for i in range(0,len(self.matriz)):
            for j in range(0,len(self.matriz[i])):
                if self.matriz[i][j] != 0:
                    self.__pinta_cuadrado(x_ini+j, y_ini+i, Cuatris.colores[self.matriz[i][j]])

    def borra(self, x_ini, y_ini):
        'borra la pieza especificada a partir de las coordenadas de malla x_ini, y_ini'
        for i in range(0,len(self.matriz)):
            for j in range(0,len(self.matriz[i])):
                if self.matriz[i][j] != 0:
                    self.__pinta_cuadrado(x_ini+j, y_ini+i, Cuatris.colores[0])

    # Movimiento de la pieza
    def mover(self, desplazamiento_x, desplazamiento_y):
        'mueve la pieza el desplazamiento indicado (sin pintarla), en coordenadas de malla'
        self.x = self.x + desplazamiento_x
        self.y = self.y + desplazamiento_y

    # Funciones que hacen uso del estado de la pieza
    def auto_pinta(self):
        'pintar la pieza en las propiedades autocontenidas'
        self.pinta(self.x, self.y)

    def auto_borra(self):
        'borrar la piezaden las propiedades autocontenidas'
        self.borra(self.x, self.y)

    def colisiona_con(self, resto):
        for i in range(0,len(self.matriz)):
            for j in range(0,len(self.matriz[i])):
                if self.matriz[i][j] != 0:
                    if resto.matriz[self.y + i][self.x + j] != 0:
                        return True
        return False

class Recipiente(Pieza):

    def __quitar_fila(self, linea):
        'retira la fila indicada, poniendo una nueva fila en la parte de arriba de la pantalla'
        for fila in range(linea, 0, -1):
            self.matriz[fila] = self.matriz[fila - 1]
        self.matriz[0] = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    def comprobar_lineas(self, otra_pieza):
        'comprueba las líneas formadas por la nueva pieza'
        lineas = 0
        for fila in range(otra_pieza.y, otra_pieza.y + otra_pieza.filas):
            producto = 1;
            for valor in self.matriz[fila]:
                producto = producto * valor
                if producto == 0:
                    break
            if producto > 0:
                lineas = lineas +1
                self.__quitar_fila(fila)
        return lineas

    def incorporar(self, otra_pieza):
        'incorpora la matriz de otra pieza a la de si mismo, devolviendo el nº de líneas que se han hecho'
        for i in range(0,len(otra_pieza.matriz)):
            for j in range(0,len(otra_pieza.matriz[i])):
                if otra_pieza.matriz[i][j] != 0:
                    self.matriz[otra_pieza.y+i][otra_pieza.x+j] = otra_pieza.matriz[i][j]
        return self.comprobar_lineas(otra_pieza)

class Cuatris:
    'Objeto Cuatris: implementa la lógica del videojuego'

    # Constantes de los colores
    BLANCO = (255,255,255)
    GRIS = (127,127,127)
    NEGRO = (0, 0, 0)
    MAGENTA = (200,0,200)
    VERDE = (0, 200, 0)
    ROJO = (200, 0, 0)
    AZUL = (0, 0, 200)
    AMARILLO = (200, 200, 0)
    CYAN = (0, 200, 200)
    NARANJA = (255, 102, 16)
    colores = [NEGRO, GRIS, CYAN, AZUL, NARANJA, VERDE, ROJO, MAGENTA, AMARILLO]



    matriz_L = [(7, 0),
                (7, 0),
                (7, 7)]

    matriz_J = [(0, 8),
                (0, 8),
                (8, 8)]

    matriz_I = [(6, 0),
                (6, 0),
                (6, 0),
                (6, 0)]

    matriz_S = [(0, 2, 2),
                (2, 2, 0)]

    matriz_Z = [(4, 4, 0),
                (0, 4, 4)]

    matriz_T = [(5, 5, 5),
                (0, 5, 0)]

    matriz_O = [(3, 3),
                (3, 3)]

    matrices = [0, 0, matriz_L, matriz_J, matriz_I, matriz_S, matriz_Z, matriz_T, matriz_O]

    matriz_siguiente = [[1, 1, 1, 1, 1, 1],
                        [1, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 1],
                        [1, 0, 0, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1]]



    # Nº de cuadros por segundo
    FPS = 60

    # Lado del cuadrado por defecto
    SLOT = 40

    # Evento de Gravedad
    GRAVEDAD = pygame.USEREVENT + 1

    # Coordenadas iniciales de las piezas
    x_ini = 4
    y_ini = 0

    def __init__(self, lado_cuadrado):
        try:
            self.slot = int(lado_cuadrado)
        except ValueError:
            # Valor por defecto
            self.slot = SLOT
        self.lineas = 0
        self.lineas_siguiente_nivel = 20
        self.nivel = 0
        self.ancho = 21*self.slot
        self.alto = 22*self.slot
        # inicializamos pygame
        pygame.init()

        # definición de la pantalla
        self.pantalla = pygame.display.set_mode((self.ancho, self.alto))
        self.pantalla.fill(Cuatris.NEGRO)
        matriz_Recipiente = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.siguiente = Recipiente (Cuatris.matriz_siguiente, self.pantalla, self.slot)
        self.siguiente.pinta(13, 0)

        self.recipiente = Recipiente (matriz_Recipiente, self.pantalla, self.slot)
        self.recipiente.pinta(0, 0)

        self.pieza = self.siguiente_pieza()
        self.pieza.pinta(4,0)
        self.pieza_siguiente = self.siguiente_pieza()
        self.pieza_siguiente.pinta(15,1)

        pygame.display.update()

        # reloj de control de refresco
        self.clock = pygame.time.Clock()

        # Evento de gravedad

        self.t_CAIDA = 70
        self.t_GRAVEDAD = 2000 #milisegundos
        pygame.time.set_timer(Cuatris.GRAVEDAD, self.t_GRAVEDAD)


    def siguiente_pieza(self):
        n_pieza = random.randint(2, 8)
        pieza = Pieza (self.matrices[n_pieza], self.pantalla, self.slot)
        return pieza

    def _imprime(self, font, cadena, left, top, color, fondo):
        text = font.render(cadena, True, color, fondo)
        textrect = text.get_rect()
        textrect.left= left
        textrect.top= top
        self.pantalla.blit(text, textrect)

    def marcador(self):
        basicfont = pygame.font.SysFont(None, self.slot)
        self._imprime(basicfont,'Líneas: '+str(self.lineas), 13*self.slot, 8*self.slot, Cuatris.BLANCO, Cuatris.NEGRO)
        self._imprime(basicfont,'Nivel: '+str(self.nivel), 13*self.slot, 9*self.slot, Cuatris.GRIS, Cuatris.NEGRO)
        self._imprime(basicfont,'Siguiente: ' + str(self.lineas_siguiente_nivel), 13*self.slot, 10*self.slot, Cuatris.GRIS, Cuatris.NEGRO)


    def juego_terminado(self):
        basicfont = pygame.font.SysFont(None, self.slot) # a refactorizar
        left = self.pantalla.get_rect().centerx - len('JUEGO T')*self.slot
        top = self.pantalla.get_rect().centery
        self._imprime(basicfont,'JUEGO TERMINADO', left, top, Cuatris.ROJO, Cuatris.GRIS)
        self._imprime(basicfont,'INTRO PARA REPETIR', left, top+self.slot, Cuatris.ROJO, Cuatris.GRIS)

    def giro(self, antihorario, pieza, recipiente):
        pieza.auto_borra()
        if antihorario:
            pieza.rotarM90()
        else:
            pieza.rotar90()
        if pieza.colisiona_con(recipiente):
            pieza.mover(-1,0)
        pieza.auto_pinta()

    def mover_derecha(self, unidades, pieza, recipiente):
        pieza.auto_borra()
        pieza.mover(unidades,0)
        if pieza.colisiona_con(recipiente):
            pieza.mover(-unidades, 0)
        pieza.auto_pinta()

    def ejecutar_juego(self):

        continuar = True

        self.marcador()

        while continuar:
            # pausa hasta el siguiente "tick" de reloj
            self.clock.tick(Cuatris.FPS)

            # detección de evento QUIT (aspa)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    continuar = False
                else:
                    # Procesar la gravedad
                    if event.type == Cuatris.GRAVEDAD:
                        self.pieza.auto_borra()
                        self.pieza.mover(0, 1)
                        if self.pieza.colisiona_con(self.recipiente):
                            pygame.time.set_timer(Cuatris.GRAVEDAD, self.t_GRAVEDAD)
                            self.pieza.mover(0,-1)
                            # L.auto_pinta()
                            # Incorporar pieza a "P"
                            self.recipiente.auto_borra()
                            self.lineas = self.lineas + self.recipiente.incorporar(self.pieza)
                            # niveles
                            if self.lineas >= self.lineas_siguiente_nivel:
                                self.nivel = self.nivel +1
                                self.lineas_siguiente_nivel = self.lineas_siguiente_nivel + 20
                                if self.t_GRAVEDAD > 100:
                                    self.t_GRAVEDAD = self.t_GRAVEDAD - 1000
                            self.marcador()
                            self.recipiente.auto_pinta()
                            self.pieza_siguiente.auto_borra()
                            self.pieza = self.pieza_siguiente
                            self.pieza.pinta(4,0)
                            self.pieza_siguiente = self.siguiente_pieza()
                            self.pieza_siguiente.pinta(15,1)
                            if self.pieza.colisiona_con(self.recipiente):
                                continuar = False
                                self.juego_terminado()
                        else:
                            self.pieza.auto_pinta()

                    if event.type == pygame.KEYDOWN:

                        # El giro de las piezas puede provocar colisiones por el lado derecho
                        if event.key == pygame.K_z:
                            self.giro(True, self.pieza, self.recipiente)

                        if event.key == pygame.K_x:
                            self.giro(False, self.pieza, self.recipiente)

                        if event.key == pygame.K_LEFT:
                            self.mover_derecha(-1,self.pieza, self.recipiente)

                        if event.key == pygame.K_RIGHT:
                            self.mover_derecha(1,self.pieza, self.recipiente)

                        # acelerar gravedad
                        if event.key == pygame.K_DOWN:
                            pygame.time.set_timer(Cuatris.GRAVEDAD, self.t_CAIDA)
                        else:
                            pygame.time.set_timer(Cuatris.GRAVEDAD, self.t_GRAVEDAD)

                    pygame.display.update()
        while True:
            # pausa hasta el siguiente "tick" de reloj
            self.clock.tick(Cuatris.FPS)
            for event in pygame.event.get():
                if event.type==pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return True
                else:
                    return False

jugar = True
while jugar == True:
    juego = Cuatris(30)
    jugar= juego.ejecutar_juego()

print ("Fin del juego")
pygame.quit()

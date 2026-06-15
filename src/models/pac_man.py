import pygame

class PacMan:
    def __init__(self, x, y, vidas, velocidad):
        self.x = x
        self.y = y
        self.vidas = vidas
        self.velocidad = velocidad
        self.radio = 9
        self.anguloBoca = 0
        self.abierta = True
        self.velocidad_animacion = 300
        self.moviendose = True
        self.direccion = "derecha"
        self.direccion_deseada = "derecha"
        power_pellet = False

        # guardo la posicion inicial de pacman para cuando pierde una vida
        self.x_inicial = x
        self.y_inicial = y

        pygame.mixer.init()
        self.sonido_comer = pygame.mixer.Sound("assets/sounds/wakawaka.mp3")
    
    def _choca(self, mapa, x, y):
        """
        Verifica si la posición (x, y) choca con una pared en el mapa
        Argumentos: mapa: el objeto del mapa que contiene la información de las paredes
                   x, y: las coordenadas a verificar
        Retorna: True si choca con una pared, False si no choca
        """
        r = self.radio
        for px, py in [
            (x + r, y),
            (x - r, y),
            (x, y + r),
            (x, y - r),
        ]:
            if mapa.pasillo_pixel(px, py):
                return True
        
        return False

    def actualizar(self, dt, mapa):
        """
        Actualiza la posición de PacMan, verifica colisiones con paredes y recoge puntos.
        Argumentos: dt: el tiempo transcurrido desde la última actualización
                   mapa: el objeto del mapa para verificar colisiones y recoger puntos
        Retorna: puntos_ganados: la cantidad de puntos ganados al recoger puntos en esta actualización
                 power_pellet: True si se recogió un superpunto, False si no
        """
        
        puntos_ganados = 0
        power_pellet = False

        col_actual = int((self.x - mapa.offset_x) // mapa.tile)
        fila_actual = int((self.y - mapa.offset_y) // mapa.tile)

        if 0 <= fila_actual < mapa.filas and 0 <= col_actual < mapa.columnas:
            if mapa.grilla[fila_actual][col_actual] == ".":
                mapa.grilla[fila_actual][col_actual] = " "
                puntos_ganados = 10  #suma 10 por punto normal
                if self.sonido_comer.get_num_channels() == 0:
                    self.sonido_comer.play()
            elif mapa.grilla[fila_actual][col_actual] == "o":
                mapa.grilla[fila_actual][col_actual] = " "
                puntos_ganados = 50 #suma 50 por superpunto
                power_pellet = True 

        col = int((self.x - mapa.offset_x) // mapa.tile)
        fila = int((self.y - mapa.offset_y) // mapa.tile)
        centro_x = mapa.offset_x + col * mapa.tile + mapa.tile / 2
        centro_y = mapa.offset_y + fila * mapa.tile + mapa.tile / 2

        margen = self.velocidad * dt + 2

        if self.direccion_deseada != self.direccion:
            if self.direccion_deseada in ("arriba", "abajo"):
                _, dy = self._destino(self.direccion_deseada, dt)
                if abs(self.x - centro_x) <= margen and not self._choca(
                    mapa, centro_x, dy
                ):
                    self.x = centro_x
                    self.direccion = self.direccion_deseada
            else:
                dx, _ = self._destino(self.direccion_deseada, dt)
                if abs(self.y - centro_y) <= margen and not self._choca(
                    mapa, dx, centro_y
                ):
                    self.y = centro_y
                    self.direccion = self.direccion_deseada

        nuevo_x, nuevo_y = self._destino(self.direccion, dt)
        if not self._choca(mapa, nuevo_x, nuevo_y):
            self.x = nuevo_x
            self.y = nuevo_y

        if self.abierta:
            self.anguloBoca += self.velocidad_animacion * dt
            if self.anguloBoca >= 35:
                self.abierta = False
        else:
            self.anguloBoca -= self.velocidad_animacion * dt
            if self.anguloBoca <= 0:
                self.abierta = True

        #si se sale por la izquierda, aparece a la derecha
        if self.x < mapa.offset_x:
            self.x = mapa.offset_x + mapa.ancho

        #si se sale por la derecha, aparece a la izquierda
        elif self.x > mapa.offset_x + mapa.ancho:
            self.x = mapa.offset_x

        return puntos_ganados, power_pellet

    def mover(self, movimiento):
        """
        Actualiza la dirección deseada de PacMan según el movimiento ingresado.
        Argumentos: movimiento: una cadena que representa la dirección deseada ("arriba", "abajo", "izquierda", "derecha")
        Retorna: Nada
        """
        
        self.direccion_deseada = movimiento.lower()

    def dibujar(self, pantalla):
        """
        Dibuja a PacMan en la pantalla con la boca abierta o cerrada según su estado de animación.
        Argumentos: pantalla: el objeto de la pantalla donde se dibujará a PacMan
        Retorna: Nada
        """
        
        rotaciones = {
            "derecha": 0,
            "izquierda": 180,
            "arriba": 90,  # angulos de rotacion del pacman
            "abajo": 270,
        }

        rotacion = rotaciones[self.direccion]
        apertura = self.anguloBoca
        puntos = [(self.x, self.y)]
        pasos = 40
        for i in range(pasos + 1):
            angulo = rotacion + apertura + (360 - 2 * apertura) * i / pasos
            v = pygame.Vector2(self.radio, 0).rotate(-angulo)
            puntos.append((self.x + v.x, self.y + v.y))

        pygame.draw.polygon(pantalla, "yellow", puntos)

    def _destino(self, direccion, dt):
        """
        Calcula la nueva posición de PacMan basada en la dirección y el tiempo transcurrido.
        Argumentos: direccion: la dirección en la que se moverá PacMan ("arriba", "abajo", "izquierda", "derecha")
        Retorna: una tupla (nuevo_x, nuevo_y) con las nuevas coordenadas de PacMan después de moverse en la dirección dada
        """
        
        x, y = self.x, self.y
        if direccion == "arriba":
            y -= self.velocidad * dt
        elif direccion == "abajo":
            y += self.velocidad * dt
        elif direccion == "derecha":
            x += self.velocidad * dt
        elif direccion == "izquierda":
            x -= self.velocidad * dt
        return x, y

    #metodo que le saca la vida
    def perder_vida(self):
        """
        Resta una vida a PacMan y lo reinicia a su posición inicial.
        Argumentos: Ninguno
        Retorna: Nada
        """
        
        self.vidas -= 1
        #vuelve a la posicion inicial
        self.x = self.x_inicial
        self.y = self.y_inicial
        #reinicia direccion
        self.direccion = "derecha"
        self.direccion_deseada = "derecha"

    def esta_vivo(self):
        """
        Verifica si PacMan aún tiene vidas restantes.
        Argumentos: Ninguno
        Retorna: True si PacMan tiene al menos una vida, False si no tiene vidas restantes
        """
        
        return self.vidas > 0

    def colisionar(self, fantasma):
        """
        Verifica si PacMan colisiona con un fantasma.
        Argumentos: fantasma: el objeto del fantasma con el que se verificará la colisión
        Retorna: True si hay una colisión entre PacMan y el fantasma, False si no hay colisión
        """
        
        distancia = ((self.x - fantasma.x) ** 2 + (self.y - fantasma.y) ** 2) ** 0.5
        return distancia < self.radio + 15
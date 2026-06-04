import pygame

class PacMan:
    def __init__ (self, x, y, vidas, velocidad):
        self.x = x
        self.y = y
        self.vidas = vidas
        self.velocidad = velocidad
        self.radio = 10
        self.direccion = "derecha"
        self.anguloBoca = 0
        self.abierta = True
        self.velocidad_animacion = 300
        self.moviendose = True
        
        #guardo la posicion inicial de pacman para cuando pierde una vida
        self.x_inicial = x
        self.y_inicial = y
        
        pygame.mixer.init()
        pygame.mixer.music.load("src/models/pacman_sound.mp3")
    
    def actualizar(self, dt, mapa):
        puntos_ganados = 0
        
        col_actual = int((self.x - mapa.offset_x) // mapa.tile)
        fila_actual = int((self.y - mapa.offset_y) // mapa.tile)
        
        if 0 <= fila_actual < mapa.filas and 0 <= col_actual < mapa.columnas:
            if mapa.grilla[fila_actual][col_actual] == ".":
                mapa.grilla[fila_actual][col_actual] = " "
                puntos_ganados = 10  # Suma 10 por punto normal
            elif mapa.grilla[fila_actual][col_actual] == "o":
                mapa.grilla[fila_actual][col_actual] = " "
                puntos_ganados = 50  # Suma 50 por superpunto
        
        if self.direccion == "arriba":
            self.y -= self.velocidad * dt
        elif self.direccion == "abajo":
            self.y += self.velocidad * dt
        elif self.direccion == "derecha":
            self.x += self.velocidad * dt
        elif self.direccion == "izquierda":
            self.x -= self.velocidad * dt

        if self.abierta:
            self.anguloBoca += self.velocidad_animacion * dt
            if self.anguloBoca >= 35:
                self.abierta = False
        else:
            self.anguloBoca -= self.velocidad_animacion * dt
            if self.anguloBoca <= 0:
                self.abierta = True
        
        # Si se sale por la izquierda, aparece a la derecha
        if self.x < mapa.offset_x:
            self.x = mapa.offset_x + mapa.ancho
        
        # Si se sale por la derecha, aparece a la izquierda
        elif self.x > mapa.offset_x + mapa.ancho:
            self.x = mapa.offset_x
        
        return puntos_ganados
    
    def mover(self, movimiento):
        self.direccion = movimiento.lower()

    def dibujar(self, pantalla):
        rotaciones = {
            "derecha": 0,
            "izquierda": 180,
            "arriba": 90, #angulos de rotacion del pacman
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

    #metodo que le saca la vida
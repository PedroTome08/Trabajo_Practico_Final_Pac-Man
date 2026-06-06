import pygame

class PacMan:
    def __init__ (self, x, y, vidas, velocidad):
        self.x = x
        self.y = y
        self.vidas = vidas
        self.velocidad = velocidad
        self.radio = 10
        self.anguloBoca = 0
        self.abierta = True
        self.velocidad_animacion = 300
        self.moviendose = True
        self.direccion = "derecha"
        self.direccion_deseada = "derecha"
        
        #guardo la posicion inicial de pacman para cuando pierde una vida
        self.x_inicial = x
        self.y_inicial = y
        
        pygame.mixer.init()
        pygame.mixer.music.load("assets/sounds/pacman_sound.mp3")

    def _choca(self, mapa, x, y):
        for px, py in [(x + self.radio, y), (x - self.radio, y), (x, y + self.radio), (x, y - self.radio)]:
            if mapa.pasillo_pixel(px, py):
                return True
        return False
    
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
        
        col = int((self.x - mapa.offset_x) // mapa.tile)
        fila = int((self.y - mapa.offset_y) // mapa.tile)
        centro_x = mapa.offset_x + col * mapa.tile + mapa.tile / 2
        centro_y = mapa.offset_y + fila * mapa.tile + mapa.tile / 2

        margen = self.velocidad * dt + 2

        if self.direccion_deseada != self.direccion:
            if self.direccion_deseada in ("arriba", "abajo"):
                _, dy = self._destino(self.direccion_deseada, dt)
                if abs(self.x - centro_x) <= margen and not self._choca(mapa, centro_x, dy):
                    self.x = centro_x
                    self.direccion = self.direccion_deseada
            else:
                dx, _ = self._destino(self.direccion_deseada, dt)
                if abs(self.y - centro_y) <= margen and not self._choca(mapa, dx, centro_y):
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
        
        # Si se sale por la izquierda, aparece a la derecha
        if self.x < mapa.offset_x:
            self.x = mapa.offset_x + mapa.ancho
        
        # Si se sale por la derecha, aparece a la izquierda
        elif self.x > mapa.offset_x + mapa.ancho:
            self.x = mapa.offset_x
        
        return puntos_ganados
    
    def mover(self, movimiento):
        self.direccion_deseada = movimiento.lower()

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

    def _destino(self, direccion, dt):
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
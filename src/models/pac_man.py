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
    
    def actualizar(self, dt):
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
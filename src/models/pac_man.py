import pygame

class PacMan:
    def __init__ (self, x, y, vidas, velocidad):
        self.x = x
        self.y = y
        self.vidas = vidas
        self.velocidad = velocidad
        self.radio = 20
        self.direccion = "derecha"
        self.anguloBoca = 0
        self.abierta = True
        self.velocidad_animacion = 200
        self.moviendose = False
    
    #función que dibuje al pacman
    
    def actualizar(self, dt):
        if not self.moviendose:
            return
        if self.abierta:
            self.anguloBoca += self.velocidad_animacion * dt
            if self.anguloBoca >= 15:
                self.abierta = False
        else:
            self.anguloBoca -= self.velocidad_animacion * dt
            if self.anguloBoca <= 0:
                self.abierta = True

    def dibujar(self, pantalla):
        rotaciones = {
            "derecha":    0,
            "izquierda": 180,
            "arriba":     90,
            "abajo":     270,
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

    def mover(self, movimiento, dt):
        self.direccion = movimiento
        self.moviendose = True
        if movimiento == "arriba":
            self.y -= self.velocidad * dt
        elif movimiento == 'abajo':
            self.y += self.velocidad * dt
        elif movimiento == 'derecha':
            self.x += self.velocidad * dt
        elif movimiento == 'izquierda':
            self.x -= self.velocidad * dt

    #metodo que le saca la vida
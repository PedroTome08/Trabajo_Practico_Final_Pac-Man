import pygame

class PacMan:
    def __init__ (self, x, y, vidas, velocidad):
        self.x = x
        self.y = y
        self.vidas = vidas
        self.velocidad = velocidad
    
    #función que dibuje al pacman
    
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, "yellow", pygame.Vector2(self.x, self.y), 20)

    def mover(self, movimiento, dt):
        if movimiento == "arriba":
            self.y -= self.velocidad * dt
        elif movimiento == 'abajo':
            self.y += self.velocidad * dt
        elif movimiento == 'derecha':
            self.x += self.velocidad * dt
        elif movimiento == 'izquierda':
            self.x -= self.velocidad * dt

    #metodo que le saca la vida
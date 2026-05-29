import pygame

class Fantasma:
    def __init__(self, x, y, puntaje, velocidad):
        self.x = x
        self.y = y
        self.puntaje = puntaje
        self.velocidad = velocidad
        
    def blinky(self, pantalla):
        pygame.draw.circle(pantalla, "red", pygame.Vector2(self.x, self.y), 20)
        #movimiento
        #el perseguidor. Su tile objetivo en Chase es la posición actual de Pac-Man.
        
    def pinky(self, pantalla):
        pygame.draw.circle(pantalla, "pink", pygame.Vector2(self.x, self.y), 20)
        #movimiento
        #el emboscador. su tile objetivo en Chase es el tile ubicado 4 posiciones adelante de la dirección actual de Pac-Man. Intenta cortarle el paso por delante.
        
    def inky(self, pantalla):
        pygame.draw.circle(pantalla, "cyan", pygame.Vector2(self.x, self.y), 20)
        #movimiento
        #el flanqueador. su tile objetivo se calcula en dos pasos: primero se toma el tile ubicado 2 posiciones adelante de Pac-Man; luego se traza un vector desde la posición de Blinky hasta ese tile y se duplica. Si Blinky no está en la partida, se utiliza al azar alguno de los otros fantasmas.
        
    def clyde(self, pantalla):
        pygame.draw.circle(pantalla, "orange", pygame.Vector2(self.x, self.y), 20)
        #movimiento
        #el tímido. si su distancia a Pac-Man es mayor a 8 tiles, su target es la posición de Pac-Man. Si está a 8 tiles o menos, su target pasa a ser su esquina de Scatter. Evita acercarse demasiado.

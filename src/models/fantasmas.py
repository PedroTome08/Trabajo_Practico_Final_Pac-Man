import pygame

class Fantasma:
    def __init__(self, x, y, nombre, color, puntaje, velocidad):
        self.x = x
        self.y = y
        self.nombre = nombre
        self.color = color
        self.puntaje = puntaje
        self.velocidad = velocidad
        
        self.img_der = pygame.image.load(f"assets/images/{nombre.lower()}_der.png").convert_alpha() #metodo de pygame para cargar imagenes de los fantasmas
        self.img_izq = pygame.image.load(f"assets/images/{nombre.lower()}_izq.png").convert_alpha()

        self.img_der = pygame.transform.scale(self.img_der, (38, 38)) #metodo de pygame para ajustar el tamaño de la imagen de los fantasmas
        self.img_izq = pygame.transform.scale(self.img_izq, (38, 38))
        
        self.direccion = "izq"
        
    def dibujar_fantasmas(self, pantalla):
        if self.direccion == "der":
            pantalla.blit(self.img_der, (self.x, self.y))
        else:
            pantalla.blit(self.img_izq, (self.x, self.y))
        
#cada fantasma hereda los atributos de la clase Fantasma
class Blinky(Fantasma):
    pass

class Pinky(Fantasma):
    pass

class Inky(Fantasma):
    pass

class Clyde(Fantasma):
    pass

class Fantasma5(Fantasma):
    pass

class Fantasma6(Fantasma):
    pass
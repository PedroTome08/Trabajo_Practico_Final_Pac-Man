import pygame

#mapa = grilla de tiles, cada tile tiene un tipo (pared, pasillo, punto, superpunto)

class Mapa:
    def __init__(self, archivo, ancho_pantalla, alto_pantalla):
        self.grilla = []
        
        with open(archivo) as mapa_txt:
            lineas = mapa_txt.readlines()
        for linea in lineas:
            self.grilla.append(list(linea.strip('\n')))
        
        ancho_maximo = max(len(fila) for fila in self.grilla)
        for fila in self.grilla:
            fila.extend([" "] * (ancho_maximo - len(fila)))

        self.columnas = ancho_maximo
        self.filas = len(self.grilla)
        self.tile = min(ancho_pantalla // self.columnas,
        alto_pantalla  // self.filas)
        self.offset_x = (ancho_pantalla - self.columnas * self.tile) // 2
        self.offset_y = (alto_pantalla - self.filas * self.tile) // 2
        self.ancho = self.columnas * self.tile
        self.alto  = self.filas * self.tile
    
    def dibujar(self, pantalla):
        t = self.tile
        for fila in range(len(self.grilla)):
            for columna in range(len(self.grilla[fila])):
                tile = self.grilla[fila][columna]
                x = self.offset_x + columna * t
                y = self.offset_y + fila * t
            
                #dibujo cada tile con su tipo
            
                if tile == "X":
                    pygame.draw.rect(pantalla, "blue", pygame.Rect(x, y, t, t))
                elif tile == "o":
                #power pellet
                    pygame.draw.circle(pantalla, "white", (x + t // 2, y + t // 2), 5) #+ t//2 para centrar el circulo en el tile
                elif tile == "G":
                    #interior de la ghost house
                    pygame.draw.rect(pantalla, "black", pygame.Rect(x, y, t, t))
                elif tile == ".":
                    #punto
                    pygame.draw.circle(pantalla, "white", (x + t // 2, y + t // 2), 2) #+ t//2 para centrar el punto en el tile
                elif tile == " ":
                    #pasillo vacio
                    pygame.draw.rect(pantalla, "black", pygame.Rect(x, y, t, t))
                elif tile == "T":
                    #tunel lateral
                    pygame.draw.rect(pantalla, "black", pygame.Rect(x, y, t, t))
                elif tile == "-":
                    #puerta de la ghost house
                    pygame.draw.line(pantalla, "purple", (x, y + t // 2), (x + t, y + t // 2), 3) #+ t//2 para centrar la linea en el tile
                #elif tile == "P":
                    #posicion inicial de pacman
                    
    def pasillo_pixel(self, x, y):
        col = int((x - self.offset_x) // self.tile)
        fil = int((y - self.offset_y) // self.tile)
        
        if 0 <= fil < self.filas and 0 <= col < self.columnas:
            return self.grilla[fil][col] == 'X'
        
        return False #si esta adentro del mapa y no es pared, es pasillo valido
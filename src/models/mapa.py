import pygame

#mapa = grilla de tiles, cada tile tiene un tipo (pared, pasillo, punto, superpunto)

class Mapa:
    def __init__(self, archivo):
        self.grilla = []
        
        with open(archivo) as mapa_txt:
            lineas = mapa_txt.readlines()
        for linea in lineas:
            self.grilla.append(list(linea.strip()))
    
    def dibujar(self, pantalla):
        for fila in range(len(self.grilla)):
            for columna in range(len(self.grilla[fila])):
                tile = self.grilla[fila][columna]
                
                #dibujo cada tile con su tipo
                
                if tile == "X":
                    pygame.draw.rect(pantalla, "blue", pygame.Rect(columna * 28, fila * 28, 28, 28))
                elif tile == "o":
                    #power pellet
                    pygame.draw.circle(pantalla, "white", (columna * 28 + 14, fila * 28 + 14), 5) #+ 14 para centrar el circulo en el tile
                elif tile == "G":
                    #interior de la ghost house
                    pygame.draw.rect(pantalla, "black", pygame.Rect(columna * 28, fila * 28, 28, 28))
                elif tile == ".":
                    #punto
                    pygame.draw.circle(pantalla, "white", (columna * 28 + 14, fila * 28 + 14), 2) #+ 14 para centrar el punto en el tile
                elif tile == " ":
                    #pasillo vacio
                    pygame.draw.rect(pantalla, "black", pygame.Rect(columna * 28, fila * 28, 28, 28))
                elif tile == "T":
                    #tunel lateral
                    pygame.draw.rect(pantalla, "black", pygame.Rect(columna * 28, fila * 28, 28, 28))
                elif tile == "-":
                    #puerta de la ghost house
                    pygame.draw.line(pantalla, "purple", (columna * 28, fila * 28 + 14), (columna * 28 + 28, fila * 28 + 14), 3) #+ 14 para centrar la linea en el tile
                #elif tile == "P":
                    #posicion inicial de pacman
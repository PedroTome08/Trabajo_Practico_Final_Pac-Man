import pygame

#mapa = grilla de tiles, cada tile tiene un tipo (pared, pasillo, punto, superpunto)

class Mapa:
    def __init__(self, grilla):
        self.grilla = grilla
        
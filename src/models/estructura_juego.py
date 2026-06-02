import pygame

#juego(puntaje, mapa, jugador, fase, fantasmas)

class Juego:
    def __init__(self, puntaje, mapa, jugador, fase, fantasmas):
        self.puntaje = puntaje
        self.mapa = mapa
        self.jugador = jugador
        self.fase = fase
        self.fantasmas = fantasmas

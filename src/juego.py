import sys
import pygame

sys.path.append("..")

from models.pac_man import PacMan
from models.mapa import Mapa

pygame.init()
ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
corriendo = True
dt = 0 #delta tiempo
mapa = Mapa("src/models/mapa_txt.txt", ANCHO, ALTO)
pacman = PacMan(x = mapa.offset_x + mapa.ancho / 2, y = mapa.offset_y + mapa.alto / 2, vidas = 3, velocidad=100)
while corriendo:
    #acá se almacenan los movimientos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
    
    #color de la pantalla
    pantalla.fill("black")
    
    #dibujo el mapa y el pacman
    mapa.dibujar(pantalla)
    pacman.dibujar(pantalla)
    
    #que pasa cuando toco las teclas AWSD para moverlo
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        pacman.mover("arriba", dt)
    if keys[pygame.K_s]:
        pacman.mover("abajo", dt)
    if keys[pygame.K_a]:
        pacman.mover("izquierda", dt)
    if keys[pygame.K_d]:
        pacman.mover("derecha", dt)

    pygame.display.flip()

    dt = reloj.tick(60) / 1000

pygame.quit()
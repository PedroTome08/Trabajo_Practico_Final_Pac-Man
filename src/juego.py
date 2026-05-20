import sys
import pygame

sys.path.append("..")

from models.pac_man import PacMan

pygame.init()
pantalla = pygame.display.set_mode((1280, 720))       
reloj = pygame.time.Clock()
corriendo = True
dt = 0 #delta tiempo
pacman = PacMan(x = pantalla.get_width() / 2, y = pantalla.get_height() / 2, vidas = 3, velocidad=100)

while corriendo:
    #acá se almacenan los movimientos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    #color de la pantalla
    pantalla.fill("black") 

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
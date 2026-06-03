import sys
import pygame

sys.path.append("..")

from models.pac_man import PacMan
from models.mapa import Mapa
from models.menu import Menu
from models.fantasmas import Fantasma
from models.estados import Estado

pygame.init()

ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
corriendo = True
#delta tiempo
dt = 0
sonido_iniciado = False
mapa = Mapa("src/models/mapa_txt.txt", ANCHO, ALTO)
menu = Menu(ANCHO, ALTO)
col = 13
fila = 23
pacman = PacMan(x = mapa.offset_x + col * mapa.tile + mapa.tile / 2, y = mapa.offset_y + fila * mapa.tile + mapa.tile / 2, vidas = 3, velocidad=100)
estado_global = Estado()

while corriendo:
    #acá se almacenan los movimientos
    for evento in pygame.event.get():
       
        if evento.type == pygame.QUIT:
            corriendo = False

        if menu.estado != "MENU_TERMINADO":
            menu.manejar_eventos(evento)
    
    if menu.estado != "MENU_TERMINADO":
        menu.actualizar(dt)
        menu.dibujar(pantalla)
    
    else:
        if not sonido_iniciado:
            pygame.mixer.music.play(-1)            
            sonido_iniciado = True
        
        #color de la pantalla
        pantalla.fill("black")
    
        #dibujo el mapa y el pacman
        mapa.dibujar(pantalla)
        
        #actualizo el reloj de los fantasmas
        estado_global.actualizar(dt)
        
        #que pasa cuando toco las teclas WASD o las flechas del teclado para moverlo
        pacman.moviendose = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            pacman.mover("arriba")
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            pacman.mover("abajo")
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            pacman.mover("izquierda")
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            pacman.mover("derecha")
        pacman.actualizar(dt, mapa)
        pacman.dibujar(pantalla)
    
    pygame.display.flip()
    dt = reloj.tick(60) / 1000

pygame.quit()
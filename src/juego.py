import sys
import pygame

sys.path.append("..")

from models.pac_man import PacMan
from models.mapa import Mapa
from models.menu import Menu
from models.fantasmas import Blinky, Pinky, Inky, Clyde, Fantasma5, Fantasma6
from models.estados import Estado

pygame.init()

ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
corriendo = True
# delta tiempo
dt = 0
sonido_iniciado = False
mapa = Mapa("src/models/mapa_txt.txt", ANCHO, ALTO)

pacman = PacMan(x=mapa.pacman_inicio_x, y=mapa.pacman_inicio_y, vidas=3, velocidad=100)

# fantasmas
blinky = Blinky(x=600, y=300, nombre="Blinky", color="red", puntaje=200, velocidad=80)
pinky = Pinky(x=620, y=300, nombre="Pinky", color="pink", puntaje=200, velocidad=80)
inky = Inky(
    x=640, y=300, nombre="Inky", color="cyan", puntaje=200, velocidad=80, compa=blinky
)
clyde = Clyde(x=660, y=300, nombre="Clyde", color="orange", puntaje=200, velocidad=80)
jose = Fantasma5(x=600, y=330, nombre="Jose", color="green", puntaje=200, velocidad=80)
nacho = Fantasma6(
    x=620, y=330, nombre="Nacho_(el mago)", color="white", puntaje=200, velocidad=80
)

menu = Menu(ANCHO, ALTO)
col = 13
fila = 23
pacman = PacMan(
    x=mapa.offset_x + col * mapa.tile + mapa.tile / 2,
    y=mapa.offset_y + fila * mapa.tile + mapa.tile / 2,
    vidas=3,
    velocidad=100,
)
estado_global = Estado()

while corriendo:
    # acá se almacenan los movimientos
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

        # color de la pantalla
        pantalla.fill("black")

        # dibujo el mapa y el pacman
        mapa.dibujar(pantalla)

        # actualizo el reloj de los fantasmas
        estado_global.actualizar(dt, False)

        # que pasa cuando toco las teclas WASD o las flechas del teclado para moverlo
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

        puntos = pacman.actualizar(dt, mapa)
        menu.high_score += puntos
        pacman.dibujar(pantalla)

        # hago que aparezcan los fantasmas en el juego
        blinky.dibujar_fantasmas(pantalla)
        blinky.actualizar(dt, mapa, pacman)

        pinky.dibujar_fantasmas(pantalla)
        pinky.actualizar(dt, mapa, pacman)

        inky.dibujar_fantasmas(pantalla)
        inky.actualizar(dt, mapa, pacman)

        clyde.dibujar_fantasmas(pantalla)
        clyde.actualizar(dt, mapa, pacman)

        jose.dibujar_fantasmas(pantalla)
        nacho.dibujar_fantasmas(pantalla)

    pygame.display.flip()
    dt = reloj.tick(60) / 1000

pygame.quit()

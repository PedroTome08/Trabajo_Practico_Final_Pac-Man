import sys
import pygame

sys.path.append("..")

from models.pac_man import PacMan
from models.mapa import Mapa
from models.menu import Menu
from models.fantasmas import Fantasma, Blinky, Pinky, Inky, Clyde, Fantasma5, Fantasma6
from models.estados import Estado

from utils.game_over import dibujar_game_over

pygame.init()

DURACION_GAME_OVER_MS = 2000
ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
corriendo = True
# delta tiempo
dt = 0
sonido_iniciado = False
mapa = Mapa("src/models/mapa_txt.txt", ANCHO, ALTO)
menu = Menu(ANCHO, ALTO)

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

fantasmas: list[Fantasma] = []

col = 13
fila = 23
pacman = PacMan(
    x=mapa.offset_x + col * mapa.tile + mapa.tile / 2,
    y=mapa.offset_y + fila * mapa.tile + mapa.tile / 2,
    vidas=3,
    velocidad=100,
)
estado_global = Estado()
config_aplicada = False
score = 0
game_over = False
victoria = False
game_over_inicio = None

ESQUINAS = {
    "Superior Izquierda": (0, 0),
    "Superior Derecha": (0, mapa.columnas - 1),
    "Inferior Izquierda": (mapa.filas - 1, 0),
    "Inferior Derecha": (mapa.filas - 1, mapa.columnas - 1),
}


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
        if not config_aplicada:
            for nombre in menu.config_final:

                if nombre == "Blinky":
                    fantasmas.append(blinky)
                elif nombre == "Pinky":
                    fantasmas.append(pinky)
                elif nombre == "Inky":
                    fantasmas.append(inky)
                elif nombre == "Clyde":
                    fantasmas.append(clyde)
                elif nombre == "Jose":
                    fantasmas.append(jose)
                elif nombre == "Nacho":
                    fantasmas.append(nacho)

            for fantasma in fantasmas:
                if fantasma.nombre in menu.config_final:

                    fantasma.esquina = ESQUINAS[menu.config_final[fantasma.nombre]]

            config_aplicada = True

        if not sonido_iniciado:
            pygame.mixer.music.play(-1)
            sonido_iniciado = True

        # color de la pantalla
        pantalla.fill("black")

        # dibujo el mapa y el pacman
        mapa.dibujar(pantalla)

        # victoria y game over

        if not pacman.esta_vivo():
            game_over = True

        if not mapa.quedas_puntos():
            victoria = True

        # pantalla game over

        if game_over:
            if game_over_inicio is None:
                game_over_inicio = pygame.time.get_ticks()

            # Dibujo la escena congelada
            pacman.dibujar(pantalla)

            for fantasma in fantasmas:
                fantasma.dibujar_fantasmas(pantalla)

            # Dibujo overlay lindo encima
            dibujar_game_over(pantalla, menu.high_score, ANCHO, ALTO)

            # Después de 2 segundos vuelvo al menú
            if pygame.time.get_ticks() - game_over_inicio >= DURACION_GAME_OVER_MS:
                pygame.mixer.music.stop()
                
                menu.estado = "INICIO"

                game_over = False
                victoria = False
                game_over_inicio = None
                config_aplicada = False
                sonido_iniciado = False
                fantasmas.clear()

                mapa = Mapa("src/models/mapa_txt.txt", ANCHO, ALTO)

                col = 13
                fila = 23
                pacman = PacMan(
                    x=mapa.offset_x + col * mapa.tile + mapa.tile / 2,
                    y=mapa.offset_y + fila * mapa.tile + mapa.tile / 2,
                    vidas=3,
                    velocidad=100,
                )

                blinky = Blinky(
                    x=600,
                    y=300,
                    nombre="Blinky",
                    color="red",
                    puntaje=200,
                    velocidad=80,
                )
                pinky = Pinky(
                    x=620,
                    y=300,
                    nombre="Pinky",
                    color="pink",
                    puntaje=200,
                    velocidad=80,
                )
                inky = Inky(
                    x=640,
                    y=300,
                    nombre="Inky",
                    color="cyan",
                    puntaje=200,
                    velocidad=80,
                    compa=blinky,
                )
                clyde = Clyde(
                    x=660,
                    y=300,
                    nombre="Clyde",
                    color="orange",
                    puntaje=200,
                    velocidad=80,
                )
                jose = Fantasma5(
                    x=600,
                    y=330,
                    nombre="Jose",
                    color="green",
                    puntaje=200,
                    velocidad=80,
                )
                nacho = Fantasma6(
                    x=620,
                    y=330,
                    nombre="Nacho_(el mago)",
                    color="white",
                    puntaje=200,
                    velocidad=80,
                )

                estado_global = Estado()

        # pantalla victoria

        elif victoria:

            fuente = pygame.font.SysFont("Courier New", 72, bold=True)

            texto = fuente.render("YOU WIN!", True, (255, 255, 0))

            pantalla.blit(
                texto,
                (
                    ANCHO // 2 - texto.get_width() // 2,
                    ALTO // 2 - texto.get_height() // 2,
                ),
            )

        # juego normal

        else:
            # actualizo el reloj de los fantasmas
            estado_global.actualizar(dt, False)

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

            # colisiones

            for fantasma in fantasmas:

                if pacman.colisionar(fantasma):
                    pacman.perder_vida()
                    break

            # TODO: PREGUNTAR PARA QUE SE USABA
            """modo = estado_global.obtener_modo()
            cambio = estado_global.actualizar(dt, False)
            if cambio:
                for i in (blinky,pinky,inky,clyde):
                    i.calcular_inversa(mapa)"""

            modo = estado_global.obtener_modo()

            # hago que aparezcan los fantasmas en el juego
            for fantasma in fantasmas:

                fantasma.dibujar_fantasmas(pantalla)
                fantasma.actualizar(dt, mapa, pacman, modo)

    pygame.display.flip()
    dt = reloj.tick(60) / 1000

pygame.quit()

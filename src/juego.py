import sys
import pygame

sys.path.append("..")

from models.pac_man import PacMan
from models.mapa import Mapa
from models.menu import Menu
from models.fantasmas import Fantasma, Blinky, Pinky, Inky, Clyde, Fantasma5, Fantasma6
from models.estados import Estado

from utils.game_over import dibujar_game_over

def centro(fila, col):
    """
    Hace el cálculo para obtener las coordenadas del centro de una casilla del mapa a partir de su fila y columna
    Argumentos: fila y columna del mapa
    Retorna: coordenadas x e y del centro de esa casilla
    """
    return (mapa.offset_x + col*mapa.tile + mapa.tile/2,
            mapa.offset_y + fila*mapa.tile + mapa.tile/2)

pygame.init()
sonido_asustado = pygame.mixer.Sound("assets/sounds/modoAsustado.mp3")
sonido_muerte = pygame.mixer.Sound("assets/sounds/muertePacman.mp3")
DURACION_GAME_OVER_MS = 2000
ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()
corriendo = True
# delta tiempo
dt = 0
sonido_iniciado = False
muerte_sonando = False
intro_lista = False
mapa = Mapa("src/models/mapa_txt.txt", ANCHO, ALTO)
menu = Menu(ANCHO, ALTO)

pacman = PacMan(
    x=mapa.pacman_inicio_x,
    y=mapa.pacman_inicio_y,
    vidas=3,
    velocidad=0.80 * 7.5 * mapa.tile,
)

# fantasmas
blinky = Blinky(x=600, y=300, nombre="Blinky", color="red", puntaje=200, velocidad=80)
pinky = Pinky(x=620, y=300, nombre="Pinky", color="pink", puntaje=200, velocidad=80)
inky = Inky(
    x=640, y=300, nombre="Inky", color="cyan", puntaje=200, velocidad=80, compa=blinky
)
clyde = Clyde(x=660, y=300, nombre="Clyde", color="orange", puntaje=200, velocidad=80)
jose = Fantasma5(x=600, y=330, nombre="Jose", color="green", puntaje=200, velocidad=80)
nacho = Fantasma6(
    x=620, y=330, nombre="Nacho", color="white", puntaje=200, velocidad=80
)

fantasmas: list[Fantasma] = []

col = 13
fila = 23
pacman = PacMan(
    x=mapa.pacman_inicio_x,
    y=mapa.pacman_inicio_y,
    vidas=3,
    velocidad=100,
)

estado_global = Estado()
config_aplicada = False
score = 0
game_over = False
victoria = False
game_over_inicio = None
PUNTAJES_FANTASMA = [200, 400, 800, 1600]
fantasmas_comidos_seguidos = 0
vida_extra_dada = False

ESQUINAS = {
    "Superior Izquierda": (0, 0),
    "Superior Derecha": (0, mapa.columnas - 1),
    "Inferior Izquierda": (mapa.filas - 1, 0),
    "Inferior Derecha": (mapa.filas - 1, mapa.columnas - 1),
}

INVERSA = {
    "arriba": "abajo",
    "abajo": "arriba",
    "izquierda": "derecha",
    "derecha": "izquierda",
}

nivel = 1

puntos_comidos =0

fuente_hud = pygame.font.SysFont("Courier New", 28)

def dibujar_hud(pantalla, score, high_score, nivel, vidas):
    """
    Dibuja el HUD con el score, high score, nivel y vidas restantes
    Argumentos: pantalla donde dibujar, score actual, high score, nivel actual y vidas restantes
    Retorna: nada, dibuja directamente en la pantalla
    """
    
    pygame.draw.rect(
        pantalla,
        (20, 20, 20),
        (0, ALTO - 80, ANCHO, 80)
    )

    pygame.draw.line(
        pantalla,
        (80, 80, 80),
        (0, ALTO - 80),
        (ANCHO, ALTO - 80),
        2
    )

    texto_score = fuente_hud.render(
        f"SCORE: {score}",
        True,
        (255,255,255)
    )

    texto_high = fuente_hud.render(
        f"HIGH SCORE: {high_score}",
        True,
        (255,255,255)
    )

    texto_nivel = fuente_hud.render(
        f"LEVEL: {nivel}",
        True,
        (255,255,255)
    )

    pantalla.blit(texto_score, (20, ALTO - 55))
    pantalla.blit(texto_high, (350, ALTO - 55))
    pantalla.blit(texto_nivel, (800, ALTO - 55))

    for i in range(vidas):
        pygame.draw.circle(
            pantalla,
            "yellow",
            (1150 + i * 30, ALTO - 40),
            12
        )


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
            umbrales = [0, 30, 60, 90]
            for i, fantasma in enumerate(fantasmas):
                fantasma.umbral = umbrales[i]
                fantasma.encerrado = (i != 0)
                fantasma.encerrado_inicial = (i!=0)

            config_aplicada = True
        if not intro_lista:
            pygame.mixer.music.load("assets/sounds/inicio.mp3")
            pygame.mixer.music.play()
            intro_lista = True

        if pygame.mixer.music.get_busy():
            pantalla.fill("black")
            mapa.dibujar(pantalla)
            pacman.dibujar(pantalla)
            for fantasma in fantasmas:
                fantasma.dibujar_fantasmas(pantalla)
            dibujar_hud(pantalla, score, menu.high_score, nivel, pacman.vidas)
            pygame.display.flip()
            dt = reloj.tick(60) / 1000
            continue

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
                
                menu.fantasmas_elegidos.clear()
                menu.config_final.clear()
                menu.opcion_actual = 0

                game_over = False
                victoria = False
                game_over_inicio = None
                config_aplicada = False
                sonido_iniciado = False
                intro_lista = False
                score = 0
                puntos_comidos = 0
                fantasmas_comidos_seguidos = 0
                vida_extra_dada = False
                fantasmas.clear()

                mapa = Mapa("src/models/mapa_txt.txt", ANCHO, ALTO)

                col = 13
                fila = 23
                pacman = PacMan(
                    x=mapa.pacman_inicio_x,
                    y=mapa.pacman_inicio_y,
                    vidas=3,
                    velocidad=100,
                )
                bx, by = centro(11, 13)
                px, py = centro(14, 12)
                ix, iy = centro(14, 13)
                cx, cy = centro(14, 14)
                blinky = Blinky(
                    x=bx,
                    y=by,
                    nombre="Blinky",
                    color="red",
                    puntaje=200,
                    velocidad=80,
                )
                pinky = Pinky(
                    x=px,
                    y=py,
                    nombre="Pinky",
                    color="pink",
                    puntaje=200,
                    velocidad=80,
                )
                inky = Inky(
                    x=ix,
                    y=iy,
                    nombre="Inky",
                    color="cyan",
                    puntaje=200,
                    velocidad=80,
                    compa=blinky,
                )
                clyde = Clyde(
                    x=cx,
                    y=cy,
                    nombre="Clyde",
                    color="orange",
                    puntaje=200,
                    velocidad=80,
                )
                jose = Fantasma5(
                    x=ix,
                    y=iy,
                    nombre="Jose",
                    color="green",
                    puntaje=200,
                    velocidad=80,
                )
                nacho = Fantasma6(
                    x=cx,
                    y=cy,
                    nombre="Nacho",
                    color="white",
                    puntaje=200,
                    velocidad=80,
                )

                estado_global = Estado()

        # pantalla victoria

        elif victoria:
            pygame.mixer.stop()
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
            if muerte_sonando:
                if pygame.mixer.get_busy():
                    pacman.dibujar(pantalla)
                    for fantasma in fantasmas:
                        fantasma.dibujar_fantasmas(pantalla)
                    dibujar_hud(pantalla, score, menu.high_score, nivel, pacman.vidas)
                    pygame.display.flip()
                    dt = reloj.tick(60) / 1000
                    continue
                else:
                    muerte_sonando = False
                    
            # actualizo el reloj de los fantasmas
            modo = estado_global.obtener_modo()
            cambio = estado_global.actualizar(dt, False)
            if cambio:
                for fantasma in fantasmas:
                    fantasma.calcular_inversa(mapa)

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

            puntos, power_pellet = pacman.actualizar(dt, mapa)
            
            score += puntos
            if puntos > 0:
                puntos_comidos += 1
                
            if score > menu.high_score:
                menu.high_score = score

            if power_pellet:
                fantasmas_comidos_seguidos = 0
                sonido_asustado.play(-1)
                for fantasma in fantasmas:
                    fantasma.activar_asustado()
                    fantasma.direccion = INVERSA[fantasma.direccion]

            pacman.dibujar(pantalla)

            #colisiones

            for fantasma in fantasmas:

                if pacman.colisionar(fantasma):
                    if fantasma.muerto:
                        continue

                    if fantasma.asustado:
                        idx = min(fantasmas_comidos_seguidos, 3)
                        score += PUNTAJES_FANTASMA[idx]
                        fantasmas_comidos_seguidos += 1
                        fantasma.muerto = True
                        fantasma.asustado = False

                    else:
                        pacman.perder_vida()
                        pygame.mixer.stop()
                        sonido_muerte.play() 
                        muerte_sonando = True
                        for f in fantasmas:
                            f.reset(mapa)
                        break
            if not vida_extra_dada and score >= 10000:
                pacman.vidas += 1
                vida_extra_dada = True
            # hago que aparezcan los fantasmas en el juego
            for fantasma in fantasmas:

                fantasma.dibujar_fantasmas(pantalla)
                fantasma.actualizar(dt, mapa, pacman, modo,puntos_comidos
                                    )

            if not any(f.asustado for f in fantasmas):
                sonido_asustado.stop()

            dibujar_hud(
                pantalla,
                score,
                menu.high_score,
                nivel,
                pacman.vidas
            )
            
    pygame.display.flip()
    dt = reloj.tick(60) / 1000

pygame.quit()

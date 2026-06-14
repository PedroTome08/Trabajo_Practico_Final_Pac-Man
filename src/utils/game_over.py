import pygame

def dibujar_game_over(pantalla, puntaje, ANCHO, ALTO):
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((120, 120, 120, 130))  # gris con alpha
    pantalla.blit(overlay, (0, 0))

    ancho_caja, alto_caja = 560, 240
    x_caja = ANCHO // 2 - ancho_caja // 2
    y_caja = ALTO // 2 - alto_caja // 2

    caja = pygame.Surface((ancho_caja, alto_caja), pygame.SRCALPHA)
    pygame.draw.rect(caja, (0, 0, 0, 190), caja.get_rect(), border_radius=28)
    pygame.draw.rect(caja, (255, 255, 255, 70), caja.get_rect(), 3, border_radius=28)

    pantalla.blit(caja, (x_caja, y_caja))

    fuente_titulo = pygame.font.SysFont("Courier New", 72, bold=True)
    fuente_puntaje = pygame.font.SysFont("Courier New", 38, bold=True)

    texto_game_over = fuente_titulo.render("GAME OVER", True, (255, 60, 60))
    texto_puntaje = fuente_puntaje.render(f"Puntaje: {puntaje}", True, (255, 255, 255))

    pantalla.blit(
        texto_game_over,
        (
            ANCHO // 2 - texto_game_over.get_width() // 2,
            y_caja + 55,
        ),
    )

    pantalla.blit(
        texto_puntaje,
        (
            ANCHO // 2 - texto_puntaje.get_width() // 2,
            y_caja + 150,
        ),
    )
#pantalla principal: high score \n el numero \n PAC - MAN
#input de presionar ENTER para jugar (tiene que parpadear)
#Elegí 4 fantasmas [n / 4]: lista con opciones
#asignar una esquina a cada uno 
#comienza el juego con las vidas abajo, con el score 
import pygame

class Menu:
    def __init__(self, alto, ancho):
        self.ancho = ancho
        self.alto = alto

        #con estado me refiero a las pantallas (la de inicio, la de selección de fantasmas, la de seleccion de las esquinas y jugar)
        self.estado = "INICIO"
        self.high_score = 0
        
        #fuentes del texto en distintos tamaños
        pygame.font.init()
        self.fuente_titulo = pygame.font.SysFont("Arial", 72, bold=True)
        self.fuente_normal = pygame.font.SysFont("Arial", 36)
        self.fuente_chica = pygame.font.SysFont("Arial", 24)
        
        #variables para que parpadee el texto de presionar enter
        self.mostrar_enter = True
        self.tiempo_parpadeo = 0
        
        self.fantasmas_disponibles = ["Blinky", "Pinky", "Inky", "Clyde", "Fantasma 5", "Fantasma 6"]       #NO OLVIDAR DE PONER LOS NOMBRES DE LOLS ULTIMOS DOS FANTASMAS
        self.fantasmas_elegidos = []
        self.esquinas_asignadas = {}
        self.opcion_actual = 0
        
    def actualizar(self, dt):
        """_summary_

        Args:
            dt (_type_): _description_
        """
        if self.estado == "INICIO":
            # como hacer que el texto parpadee cada medio segundo
            self.tiempo_parpadeo += dt
            if self.tiempo_parpadeo >= 0.5:
                self.mostrar_enter = not self.mostrar_enter
                self.tiempo_parpadeo = 0
    
    #def manejar_eventos(self, eventos):
        # hay que usar algo así: 
        # ticksLastFrame = pygame.time.get_ticks()
        # delta_time = 1 / FPS
    
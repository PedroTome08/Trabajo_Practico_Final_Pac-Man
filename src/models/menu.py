#pantalla principal: high score \n el numero \n PAC - MAN
#input de presionar ENTER para jugar (tiene que parpadear)
#Elegí 4 fantasmas [n / 4]: lista con opciones
#asignar una esquina a cada uno 
#comienza el juego con las vidas abajo, con el score 
import pygame

class Menu:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

        #con estado me refiero a las pantallas (la de inicio, la de selección de fantasmas, la de seleccion de las esquinas y menu terminado)
        self.estado = "INICIO"
        self.high_score = 0
        
        #fuentes del texto en distintos tamaños
        pygame.font.init()
        self.fuente_titulo = pygame.font.SysFont("Courier New", 72, bold=True)
        self.fuente_normal = pygame.font.SysFont("Courier New", 36)
        self.fuente_chica = pygame.font.SysFont("Courier New", 24)
        
        #variables para que parpadee el texto de presionar enter
        self.mostrar_enter = True
        self.tiempo_parpadeo = 0
        
        self.fantasmas_elegidos = []
        self.esquinas = ["Superior Izquierda", "Superior Derecha", "Inferior Izquierda", "Inferior Derecha"]
        self.opcion_actual = 0
        #guarda a cada fantasma con su esquina
        self.config_final = {} 
        
        self.fantasmas_info = [
            {"id": 1, "nombre": "Blinky", "color": (255, 0, 0), "desc": "Rojo - El Perseguidor"},
            {"id": 2, "nombre": "Pinky", "color": (255, 182, 193), "desc": "Rosa - El Emboscador"},
            {"id": 3, "nombre": "Inky", "color": (0, 255, 255), "desc": "Celeste - El Flanqueador"},
            {"id": 4, "nombre": "Clyde", "color": (255, 165, 0), "desc": "Naranja - El Tímido"},
            #falta crear los fantasmas 5 y. 6
            #les puse temporalmente el mismo color porque si dejaba el (0, 0, 0) no iban a verse en la pantalla por ser de color negro
            {"id": 5, "nombre": "José", "color": (34, 139, 34), "desc": "agregar - descripcion"},
            {"id": 6, "nombre": "Nacho (el mago)", "color": (255, 255, 255), "desc": "agregar - descripcion"}
        ]
        
    def actualizar(self, dt: float):
        """_summary_

        Argumentos:
            dt (float): _description_
        """
        if self.estado == "INICIO":
            #como hacer que el texto parpadee cada medio segundo
            self.tiempo_parpadeo += dt
            
            if self.tiempo_parpadeo >= 0.5:
                self.mostrar_enter = not self.mostrar_enter
                self.tiempo_parpadeo = 0
    
    def manejar_eventos(self, evento):
        #si el usuario no presiona ninguna tecla, sale de la funcion
        if evento.type != pygame.KEYDOWN:
             return
        
        if self.estado == "INICIO":
            #si el usuario presiona enter
            if evento.key == pygame.K_RETURN:
                #pasa a la seleccion de fantasmas
                self.estado = "SELECCION_FANTASMAS"
                
        elif self.estado == "SELECCION_FANTASMAS":
            
            #hago un if que se ejecute si el usuario apreta una tecla del 1 al 6 para elegir fantasmas
            if pygame.K_1 <= evento.key <= pygame.K_6:
                #indice que hace referencia al "id" de cada fantasma en su diccionario en self.fantasmas_info
                indice = evento.key - pygame.K_1
                
                if indice in self.fantasmas_elegidos:
                    self.fantasmas_elegidos.remove(indice)
                
                #si el usuario todavia no eligio los 4 fantasmas, puede elegir otro
                elif len(self.fantasmas_elegidos) < 4: 
                    self.fantasmas_elegidos.append(indice)
            
            #si el usuario apreta enter y ya eligio los 4 fantasmas, pasa a la seleccion de esquinas
            elif evento.key == pygame.K_RETURN and len(self.fantasmas_elegidos) == 4: 
                self.estado = "SELECCION_ESQUINAS"
                self.opcion_actual = 0 #reseteo la opcion actual para que empiece desde el primer fantasma elegido en la seleccion de esquinas
        
        elif self.estado == "SELECCION_ESQUINAS":
            
            #si el usuario apreta una tecla del 1 al 4 para elegir la esquina de cada fantasma
            if pygame.K_1 <= evento.key <= pygame.K_4: 
                    #indice que hace referencia a la esquina elegida para cada fantasma
                    indice_esquina = evento.key - pygame.K_1
                    indice_fantasma = self.fantasmas_elegidos[self.opcion_actual]
                    nombre_fantasma = self.fantasmas_info[indice_fantasma]["nombre"]
                    
                    #para no repetir esquinas
                    if self.esquinas[indice_esquina] not in self.config_final.values():
                        #guarda cada fantasma con su esquina en el diccionario vacio config_final
                        self.config_final[nombre_fantasma] = self.esquinas[indice_esquina]
                        self.opcion_actual += 1
                    
                    if self.opcion_actual >= 4:
                        self.estado = "MENU_TERMINADO"
            
        elif self.estado == "MENU_TERMINADO":
            pass #creo que aca falta algo
        
        # ticksLastFrame = pygame.time.get_ticks()
        # delta_time = 1 / FPS
    
    def dibujar(self, pantalla):
        #pantalla negra
        pantalla.fill((0, 0, 0))
        
        if self.estado == "INICIO":
            self.dibujar_inicio(pantalla)
        elif self.estado == "SELECCION_FANTASMAS":
            self.dibujar_seleccion_fantasmas(pantalla)
        elif self.estado == "SELECCION_ESQUINAS":
            self.dibujar_seleccion_esquinas(pantalla)
    
    def dibujar_inicio(self, pantalla):
        texto_arriba = self.fuente_chica.render("HIGH SCORE", True, (120, 120, 120))
        texto_score = self.fuente_chica.render(str(self.high_score), True, (0, 255, 0)) #?
        texto_titulo = self.fuente_titulo.render("PAC-MAN", True, (255, 255, 0))
        
        pantalla.blit(texto_arriba, (self.ancho // 2 - texto_arriba.get_width() // 2, 80))
        pantalla.blit(texto_score, (self.ancho // 2 - texto_score.get_width() // 2, 110))
        pantalla.blit(texto_titulo, (self.ancho // 2 - texto_titulo.get_width() // 2, self.alto // 2 - 60))
        
        if self.mostrar_enter:
            texto_enter = self.fuente_normal.render("Presioná ENTER para jugar", True, (255, 255, 255))
            pantalla.blit(texto_enter, (self.ancho // 2 - texto_enter.get_width() // 2, self.alto // 2 + 80))

    def dibujar_seleccion_fantasmas(self, pantalla):
        cant = len(self.fantasmas_elegidos)
        texto_titulo = self.fuente_normal.render(f"Elegí 4 fantasmas [{cant}/4]", True, (255, 255, 0))
        pantalla.blit(texto_titulo, (self.ancho // 2 - texto_titulo.get_width() // 2, 60))
        
        start_y = 160
        separacion = 65
        
        for i, f in enumerate(self.fantasmas_info):
            y_pos = start_y + i * separacion
            
            #circulo de color de los fantasmas
            pygame.draw.circle(pantalla, f["color"], (self.ancho // 2 - 200, y_pos + 15), 14)
            
            #texto de descripcion
            color_texto = (255, 255, 255) if i in self.fantasmas_elegidos else (120, 120, 120)
            texto_opcion = f"{f['id']} {f['nombre']}"
            texto_f = self.fuente_normal.render(texto_opcion, True, color_texto)
            pos_x_nombre = self.ancho // 2 - 160
            pantalla.blit(texto_f, (pos_x_nombre, y_pos))
            
            #subtexto de la descripcion de los fantasmas
            texto_desc = self.fuente_chica.render(f"— {f['desc'].split(' - ')[1]}", True, (100, 100, 100))
            #toma la posición X del nombre, le suma el ancho exacto del nombre y le suma 20 píxeles de margen
            pos_x_desc = pos_x_nombre + texto_f.get_width() + 20 
            pantalla.blit(texto_desc, (pos_x_desc, y_pos + 6))
            
            #recuadro blanco si esta seleccionado
            if i in self.fantasmas_elegidos:
                pygame.draw.rect(pantalla, (255, 255, 255), (self.ancho // 2 - 230, y_pos - 8, 550, 48), 2)
        
    def dibujar_seleccion_esquinas(self, pantalla):
        fantasma_indice = self.fantasmas_elegidos[self.opcion_actual]
        f = self.fantasmas_info[fantasma_indice]
        
        #titulo dinamico que adopta el color del fantasma actual
        texto_titulo = self.fuente_normal.render(f"Asigná una esquina a {f['nombre']} ({self.opcion_actual + 1}/4)", True, f['color'])
        pantalla.blit(texto_titulo, (self.ancho // 2 - texto_titulo.get_width() // 2, 60))
        
        start_y = 180
        separacion = 55
        
        for i, esquina in enumerate(self.esquinas):
            
            if esquina in self.config_final.values():
                color = (80, 80, 80)
            else:
                color = (255, 255, 255)
            
            texto_esquina = self.fuente_normal.render(f'{i+1}. {esquina}', True, color)
            pantalla.blit(texto_esquina, (self.ancho // 2 - 180, start_y + i * separacion))
            
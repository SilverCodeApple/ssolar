import pygame
import numpy as np
import calculo_num as calc
import random as rn
from botones_texto import Texto, Boton
from lectura import datos_iniciales


class game:
    ##Variables
    tamano = (1280, 720)
    running = True
    radios = 6
    h = 0.001
    def __init__(self,num):
        self.iniciar(num)
        self.inicializar_cuerpos(num)
        self.propiedades_cuerpos(num)
    
    def iniciar(self,num):
        pygame.init()
        pygame.display.set_caption("Simulación")
        self.num = num
        G = 6.67430 * 10**(-11)  
        masa_solar = 1.989e30 
        anio_segundos = 31556952  
        distancia_media = 1.496e11
        ua = 100
        self.G = G * masa_solar * (anio_segundos**2) * (1/(distancia_media**3)) * (ua**3)
        self.screen = pygame.display.set_mode(self.tamano)
        self.lineas = pygame.Surface(self.tamano,pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.clock.tick(60) 
        
    def inicializar_cuerpos(self,num):
        self.posiciones = np.zeros((num,2))
        self.velocidades = np.zeros_like(self.posiciones)
        self.momento_angular = np.zeros(num)
        self.masas = np.zeros(num)
        self.colores = np.zeros((num,3))
        
        for i in range(num):
            self.colores[i] = np.array([rn.randint(0,255),rn.randint(0,255),rn.randint(0,255)])
    
    def propiedades_cuerpos(self,num):
        self.masas,self.velocidades,self.posiciones,self.colores = datos_iniciales("condiciones/datos.csv",num)
        self.obj_calc = calc.CalculoNumerico(self.posiciones, self.velocidades,
                                             self.masas,self.num, self.G, self.h)
    ### Accesors
    
    ## Events
    def events(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.running = False
    ##Funciones
    def clear(self):
        self.screen.fill((0,0,0))
    def limpiar_cerca(self,matriz, radio):
        for i in range(self.num):
            self.circulo(matriz[i],[0,0,0],radio)
    
    def linea(self,matriz,color):
        for i in range(self.num):
            pygame.draw.circle(self.lineas,(color[i][0] ,color[i][1],color[i][2]),
                                (matriz[i][0], matriz[i][1]), 2)
        self.screen.blit(self.lineas, (0, 0))
    
    def circulo(self, vector, color, radio):
        pygame.draw.circle(self.screen, (color[0] ,color[1],color[2]),(vector[0],vector[1]),radio, width=0)
    
    def movimiento_planeta(self):
        
        self.posiciones  = self.obj_calc.euler()
        #print(self.posiciones)
        self.velocidades = self.obj_calc.get_velocidades()

    def manejo_texto(self,string,vector,color):
        obj_texto = Texto()
        texto_fuente,superficie = obj_texto.mostrar_texto(vector, string, color)
        self.screen.blit(texto_fuente,superficie.topleft)
    ###Update
    def update(self):
        self.clear()
        
        self.movimiento_planeta()
        self.manejo_texto(str(self.clock.get_fps()) , [300, 720/2], [255,255,255])
        
        self.linea(self.posiciones, self.colores)
        for i in range(self.num):
            self.circulo(self.posiciones[i],self.colores[i], 10)
            
    ##Render
    def render(self):
        pygame.display.flip()

    ## Gameloop
    def gameloop(self):
        while self.running:
            self.events()
            self.update()
            self.render()
            self.clock.tick(120) 
        pygame.QUIT


if __name__ == "__main__":
    juego = game(9)
    juego.gameloop()
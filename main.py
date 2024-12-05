import pygame
import numpy as np
import calculo_num as calc
import random as rn
from botones_texto import Texto, Boton
from lectura import datos_iniciales
import time as tm

class game:
    ##Variables
    tamano = (1280, 720)
    running = True
    radios = 6
    h = 0.001
    def __init__(self,num):
        self.iniciar(num)
        self.iniciar_pantalla(num)
        self.inicializar_cuerpos(num)
        self.propiedades_cuerpos(num)
        
    
    def iniciar(self,num):
        self.num = num
        G = 6.67430 * 10**(-11)  
        masa_solar = 1.989e30 
        anio_segundos = 31556952  
        distancia_media = 1.496e11
        ua = 100
        self.G = G * masa_solar * (anio_segundos**2) * (1/(distancia_media**3)) * (ua**3)
        
    def iniciar_pantalla(self,num):
        pygame.init()
        pygame.display.set_caption("Simulación")
        self.screen = pygame.display.set_mode(self.tamano)
        self.lineas = pygame.Surface(self.tamano,pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.clock.tick(60) 
        self.tiempo = tm.time()
        self.colores = np.zeros((num,3))
        self.botones_planetas = [Boton() for i in range(num)]
        self.botones_tiempo = [Boton(), Boton(), Boton()]
        self.multiplicador = 1
        self.pausa_flag = False


    def inicializar_cuerpos(self,num):
        self.posiciones = np.zeros((num,2))
        self.velocidades = np.zeros_like(self.posiciones)
        self.momento_angular = np.zeros(num)
        self.masas = np.zeros(num)
        self.radio = 10
        
    def propiedades_cuerpos(self,num):
        self.masas,self.velocidades,self.posiciones,self.colores,self.nombres = datos_iniciales("condiciones/datos.csv",num)
        self.obj_calc = calc.CalculoNumerico(self.posiciones, self.velocidades,
                                             self.masas,self.num)
    ### Accesors
    def manejo_texto(self,string,vector,color):
        obj_texto = Texto()        
        texto_fuente,superficie = obj_texto.mostrar_texto(vector, string, color)
        self.screen.blit(texto_fuente,superficie.topleft)
    ## Events
    def events(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.running = False
            if(event.type == pygame.MOUSEWHEEL):
                print(event.x,"   ",event.y)
    def escalar(self,proporcion):
        self.posiciones /= proporcion
        self.velocidades /= proporcion
        self.radio/=proporcion
        print(self.posiciones)
    ##Funciones
    def manejo_tiempo(self,tamaño):
        textos_tiempo_nombre = ["Atras", "Parar", "Adelantar"]
        posicion_boton = [[self.tamano[0] - tamaño[0] - 400,100], [self.tamano[0] - tamaño[0] - 200,100] ,[self.tamano[0] - tamaño[0], 100] ]
        for i in range(len(self.botones_tiempo)):
            self.botones_tiempo[i].propiedades(textos_tiempo_nombre[i], [0,0,0],posicion_boton[i], tamaño,[74,66,76])
            texto, superficie, rectangulo = self.botones_tiempo[i].crear_boton()
            self.screen.blit(rectangulo, superficie)
            self.screen.blit(texto, superficie)
        if(tm.time() - self.tiempo>= 0.1):
            if(self.botones_tiempo[0].estado()):
                    self.multiplicador-= 0.1
            if(self.botones_tiempo[1].estado()):
                    if(self.pausa_flag):
                        self.multiplicador = 1
                        self.pausa_flag = False
                    else:
                        self.multiplicador = 0
                        self.pausa_flag = True
            if(self.botones_tiempo[2].estado()):
                    self.multiplicador += 0.1
        
            self.h = 0.001 * self.multiplicador
            self.tiempo = tm.time()

            
        
    def clear(self):
        self.screen.fill((0,0,0))
    def quitar_lineas(self):
        self.lineas.fill((0,0,0))
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
        self.posiciones  = self.obj_calc.euler(self.h,self.G)
        self.velocidades = self.obj_calc.get_velocidades()

    
    def botones_nombres_planeta(self,nombre,posicion,tamaño,indice):
        
        self.botones_planetas[indice].propiedades("",self.colores[indice],posicion,tamaño,self.colores[indice])

        texto, superficie,rectangulo = self.botones_planetas[indice].crear_boton()
        self.screen.blit(texto, superficie.topleft)
        
        
        if(self.botones_planetas[indice].estado()):
            self.manejo_texto(nombre,posicion,[255,255,255])
        
    
    ###Update
    def update(self):
        print(self.posiciones)
        self.clear()
        self.movimiento_planeta()
        #print(self.clock.get_fps())
        
        self.linea(self.posiciones, self.colores)
        self.limpiar_cerca(self.posiciones,self.radio+5)
        for i in range(self.num):
            self.circulo(self.posiciones[i],self.colores[i], self.radio)
            self.botones_nombres_planeta(self.nombres[i], self.posiciones[i],[20,20],i)
            self.manejo_tiempo([100,50])
            
    ##Render
    def render(self):
        pygame.display.flip()

    ## Gameloop
    def gameloop(self):
        self.escalar(2)
        while self.running:
            self.events()
            self.update()
            self.render()
            self.clock.tick(120) 
        pygame.QUIT


if __name__ == "__main__":
    juego = game(9)
    juego.gameloop()
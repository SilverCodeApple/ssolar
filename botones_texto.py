import pygame

class Texto:
    def __init__(self):
        pygame.font.init()  # Inicializar fuentes
        self.fuente = pygame.font.SysFont("calibri", 24)

    def mostrar_texto(self, vector, dato,color_texto):
        texto_fuente = self.fuente.render(dato, True, (color_texto[0],color_texto[1],color_texto[2]))
        superficie_texto = texto_fuente.get_rect(center=(vector[0], vector[1]))
        return texto_fuente, superficie_texto

    def posicion_mouse(self):
        return pygame.mouse.get_pos()

    def clicks(self):
        return pygame.mouse.get_pressed(num_buttons=3)

class Boton(Texto):
    def __init__(self, posicion, tamaño, texto,color_texto, color_recuadro):
        super().__init__()
        self.rectangulo = pygame.Surface((tamaño[0],tamaño[1]))
        self.rectangulo.fill((color_recuadro[0],color_recuadro[1],color_recuadro[2]))
        self.posicion = posicion
        self.color_texto = color_texto
        self.tamano = tamaño
        self.texto = texto

    def crear_boton(self):
        texto_fuente, superficie_texto = self.mostrar_texto(self.posicion, self.texto,self.color_texto)
        return texto_fuente, superficie_texto,self.rectangulo

    def estado(self):
        posicion = self.posicion_mouse()
        clicks = self.clicks()
        if (
            self.posicion[0] - self.tamano[0] // 2 < posicion[0] < self.posicion[0] + self.tamano[0] // 2
            and self.posicion[1] - self.tamano[1] // 2 < posicion[1] < self.posicion[1] + self.tamano[1] // 2
            and clicks[0]
        ):
            return True
        return False

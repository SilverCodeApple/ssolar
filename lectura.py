import numpy as np

def datos_iniciales(nombre_archivo,numero):
    informacion = np.genfromtxt(nombre_archivo, delimiter=',', names=True, dtype=None, encoding='utf-8')
    nombres = informacion["Planeta"]
    masas = informacion["Masa"]
    
    color = []
    velocidad = []
    posicion = []
    
    
    for i in range(numero):
        velocidad.append([informacion["Vx"][i], informacion["Vy"][i]])
        posicion.append([informacion["Posx"][i] , informacion["Posy"][i]])
        color.append([informacion["R"][i],informacion["G"][i],informacion["B"][i]])
    
    return masas, np.array(velocidad), np.array(posicion),np.array(color), nombres

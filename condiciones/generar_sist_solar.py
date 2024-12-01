import numpy as np

datos = np.genfromtxt("condiciones/datos_sistema_solar.csv", delimiter=',', names=True, dtype=None, encoding='utf-8')

semieje_menor = datos["Mayor"]*np.sqrt(1-datos["Excentricidad"]**2)




periodos = datos["T"] ##Años
angulos = [0,0,0,0,0,180,225,270,315]
eje_de_referencia = [1280//2,720//2]
masas = datos["Masa"]
nombres = datos["Planeta"]
ua = 100#px
G = 6.67430 * 10**(-11)*(1.989e30)*(31556952**2)*(1/(1.496e11)**3)
momento_angular = datos["Momento_angular"]*(1/1.989e30)*(1/(149597828677**2))*(31556952)
masa_reducida = []
posicion = []
velocidad = []
print(momento_angular)
for i in range(len(masas)):
    masa_reducida.append(masas[0]*masas[i]/(masas[0]+masas[i]))
    r = np.sqrt((semieje_menor[i]*np.cos(np.deg2rad(angulos[i])))**2 + (datos["Mayor"][i]*np.sin(np.deg2rad(angulos[i]))) **2)
    
    if(semieje_menor[i] != 0):
        magnitud = momento_angular[i]/((r**2)*masa_reducida[i])*r
        
    else:
        magnitud = 0
    
    velocidad.append([-magnitud*np.sin(np.deg2rad(angulos[i])),magnitud*np.cos(np.deg2rad(angulos[i]))])
    posicion.append([semieje_menor[i]*ua*np.cos(np.deg2rad(angulos[i])) + eje_de_referencia[0],datos["Mayor"][i]*ua*np.sin(np.deg2rad(angulos[i]))+ eje_de_referencia[1]])
header = "Planeta,Vx,Vy,Posx,Posy,Masa"

with open("condiciones/datos.csv","w",encoding= "utf-8") as file:
    file.write(header)
    for i in range(len(masas)):
        file.write(f"\n{nombres[i]},{velocidad[i][0]},{velocidad[i][1]},{posicion[i][0]},{posicion[i][1]},{masas[i]}")
    






















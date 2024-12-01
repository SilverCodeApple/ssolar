import numpy as np

datos = np.genfromtxt("datos_sistema_solar.csv", delimiter=',', names=True, dtype=None, encoding='utf-8')


semieje_menor = datos["Mayor"]*np.sqrt(1-datos["Excentricidad"]**2)
omega = datos["T"]

for i in range(len(omega)):
    if(omega[i]!= 0):
        omega[i] = 2*np.pi/np.array(omega[i])    
    

angulos = [0,0,45,90,135,180,225,270,315]
eje_de_referencia = [1280//2,720//2]
posicion = []
velocidad = []

ua = 100#px
G = 6.67430 * 10**(-11)*(1.989e30)*(31556952**2)*(1/(1.496e11)**3)*(100*3)

masas = datos["Masa"]
masa_reducida = masas[0]*masas[1]/(masas[0]+ masas[1])

momento_angular = 9.1e38 * (1/1.989e30)*(31556952)*(1/(1.496e11)**3)*(100**2)

t1 = momento_angular/masa_reducida

def distancia(r):
    d = np.sqrt(r[0]**2 + r[1]**2)
    if (d==0):
        return 100000000000
    else:
        return d

for i in range(len(datos["Mayor"])):
    posicion.append([semieje_menor[i]*ua*np.cos(np.deg2rad(angulos[i])),datos["Mayor"][i]*ua*np.sin(np.deg2rad(angulos[i]))])
    velocidad.append([-t1*(semieje_menor[i]/(distancia(posicion[i])))*ua*np.sin(np.deg2rad(angulos[i])), 
                      t1*(datos["Mayor"][i]/(distancia(posicion[i])))*ua*np.cos(np.deg2rad(angulos[i]))])
posicion = np.array(posicion)+np.array(eje_de_referencia)
velocidad = np.array(velocidad)

print(velocidad)





valores = np.column_stack((datos["Planeta"], velocidad[:,0],velocidad[:,1] , posicion[:,0],posicion[:,1],datos["Masa"]))

encabezado = "Planeta,Vx,Vy,Posx,Posy,Masa"
with open("datos.csv","w",encoding= "utf-8") as archivo:
    archivo.write(encabezado)
    archivo.write("\n")
    for i in valores:
        for j in i:
            archivo.write(str(j) + ",")
        archivo.write("\n")


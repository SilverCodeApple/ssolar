import numpy as np

datos = np.genfromtxt("condiciones/datos_sistema_solar.csv", delimiter=',', names=True, dtype=None, encoding='utf-8')

semieje_menor = datos["Mayor"]*np.sqrt(1-datos["Excentricidad"]**2)

periodos = datos["T"] ##Años
angulos = [0,12,34,65,76,180,225,270,315]
eje_de_referencia = [1280//2,720//2]
masas = datos["Masa"]
nombres = datos["Planeta"]
ua = 100#px
G = 6.67430 * 10**(-11)*(1.989e30)*(31556952**2)*(1/(1.496e11)**3)*(ua**3)

momento_angular = datos["Momento_angular"]*(1/1.989e30)*(1/(149597828677**2))*(31556952)*(ua**2)
masa_reducida = []
omega = []
for i in range(len(periodos)):
    masa_reducida.append(masas[0]*masas[i]/(masas[i]+masas[0]))
    r = np.sqrt((semieje_menor[i]*ua*np.cos(np.deg2rad(angulos[i])))**2 + (datos["Mayor"][i]*ua*np.sin(np.deg2rad(angulos[i]))) **2)
    if(periodos[i]!=0):
        omega.append(2*np.pi/periodos[i])
    else:
        omega.append(0)


posicion = []
velocidad = []

for i in range(len(masas)):
    if(datos["Planeta"][i] == "Venus"):
        velocidad.append([semieje_menor[i]*omega[i]*ua*np.sin(np.deg2rad(angulos[i])),-datos["Mayor"][i]*omega[i]*ua*np.cos(np.deg2rad(angulos[i]))])
    else:
        velocidad.append([-semieje_menor[i]*omega[i]*ua*np.sin(np.deg2rad(angulos[i])),datos["Mayor"][i]*omega[i]*ua*np.cos(np.deg2rad(angulos[i]))])
    posicion.append([semieje_menor[i]*ua*np.cos(np.deg2rad(angulos[i])) + eje_de_referencia[0],datos["Mayor"][i]*ua*np.sin(np.deg2rad(angulos[i]))+ eje_de_referencia[1]])

colores_planetas = [
    [255, 204, 0],    # Sol (amarillo brillante)
    [169, 169, 169],  # Mercurio (gris)
    [255, 160, 122],  # Venus (rosado claro)
    [0, 0, 255],      # Tierra (azul)
    [255, 69, 0],     # Marte (rojo)
    [202, 169, 57],    # Júpiter (dorado)
    [210, 180, 140],  # Saturno (arena)
    [0, 191, 255],    # Urano (azul claro)
    [0, 0, 139]       # Neptuno (azul oscuro)
]


header = "Planeta,Vx,Vy,Posx,Posy,Masa,R,G,B"
print(velocidad)

with open("condiciones/datos.csv","w",encoding= "utf-8") as file:
    file.write(header)
    for i in range(len(masas)):
        file.write(f"\n{nombres[i]},{velocidad[i][0]},{velocidad[i][1]},{posicion[i][0]},{posicion[i][1]},{masas[i]},{colores_planetas[i][0]},{colores_planetas[i][1]},{colores_planetas[i][2]}")























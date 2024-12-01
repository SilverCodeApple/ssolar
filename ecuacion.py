import numpy as np

class calculo_num:
    h = 0.1
    def inicio(self, masas, matriz_posicion, velocidades,momento_angular):
        self.cantidad = len(matriz_posicion[:,0])
        self.masas = masas
        self.posiciones = matriz_posicion
        self.velocidades = velocidades
        self.momento_angular = momento_angular
    
    def __init__(self,masas,matriz_posicion,velocidades,momento_angular):
        self.inicio(masas,matriz_posicion,velocidades,momento_angular)    
    def magnitud(self,r):
        return np.sqrt(r[0]**2 + r[1]**2)
    def direccion(self,r1,r2):
        r = r1 - r2
        r_hat = r/self.magnitud(r)
        return r_hat
    def distancia(self,r1,r2):
        return np.sqrt((r1[0] - r2[0])**2 + (r1[1] - r2[1])**2)
    
    def ecuaciones(self):
        G = 6.67430 * 10**(-11)*(1.989e30)*(31556952**2)*(1/(1.496e11)**3)*(100*3)  
        dv_dt = np.zeros((self.cantidad,2))
        for i in range(self.cantidad):
            suma = 0
            for j in range(self.cantidad):
                if j!=i:
                    r = self.distancia(self.posiciones[i],self.posiciones[j])**2
                    if(r!=0):
                        suma=G*self.masas[j]/r
                        suma*= self.direccion(self.posiciones[j], self.posiciones[i])
                    else:
                        suma = 0
            dv_dt[i] = suma
    
        return dv_dt
    
    def metodo_euler(self):
        dv_dt  = self.ecuaciones()
        for i in range(self.cantidad):
            self.velocidades[i] = dv_dt[i]*self.h + self.velocidades[i]
            self.posiciones[i] = self.velocidades[i]*self.h + self.posiciones[i]
            self.momento_angular[i] = self.magnitud(self.velocidades[i])*self.masas[i]*self.distancia(self.posiciones[i],[1280/2,720/2])
            
        return self.posiciones, self.velocidades,self.momento_angular







import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import *

class rectangle:
    def __init__(self,longueur_precision_spaciale,raideur,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G):
        self.len = longueur_precision_spaciale
        self.stif = raideur
        self.dim = dimensions
        self.mass = mass
        self.position = position_initial
        self.start = positions_de_qlq_points
        self.alpha = alpha
        self.vit = vitesse_de_G

    def simuler(self,temps_de_la_simulation,precision_dt,scale):
        t = temps_de_la_simulation
        dt = precision_dt
        s=scale

        alpha = self.alpha
        l = self.len
        d = l*np.sqrt(2)
        k = self.stif
        a = np.floor(self.dim[0]/l)*l
        b = np.floor(self.dim[1]/l)*l
        x = self.position[0]
        y = self.position[1]

        def A(L,i,j): #une fonction qui aidera á bien organiser les points de la matrice
            return L[i][j]

        #M est la matrice representant les points du solide

        M = []
        V = []
        nombre_de_points=0
        for i in range(0,int(b/l)):
            L=[]
            K=[]
            for j in range(int(a/l)):
                nombre_de_points+=1
                L.append([x+l*j,y+l*i])
                K.append(self.vit)
            M.append(L)
            V.append(K)

        m = self.mass/nombre_de_points

        #maintenant on reorganise quelque points suivant les commande de positions_de_qlq_points

        for k in self.start:
            i=k[0]
            j=k[1]
            M[i][j]=k[2:]

        W = 800
        H = 500
        window = Tk()
        canvas = Canvas(window, width=W, height=H, bg="grey")
        canvas.pack()

        def dessine_point(A):
            canvas.create_rectangle(A[0]*s-3,A[1]*s+3,A[0]*s+4,A[1]*s-4,fill="black")

        def dessine_les_points_de_la_matrice(M):
            for i in M:
                for A in i:
                    dessine_point(A)

        def dessine_ligne_entre(A,B):
            canvas.create_line(A[0]*s,B[0]*s,A[1]*s,B[1]*s,fill="red")

        def dessine_lignes(M):
            for i in range(0,len(M)):
                for j in range(0,len(M[0])):
                    if i!=len(M)-1:

                        if j==0:

                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j))
                            dessine_ligne_entre(A(M, i, j), A(M, i, j + 1))
                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j + 1))

                        if j!=0 and j!=len(M[0])-1:

                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j))
                            dessine_ligne_entre(A(M, i, j), A(M, i, j + 1))
                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j + 1))
                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j - 1))

                        if j==len(M[0])-1:

                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j))
                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j - 1))

                    if i==len(M)-1:
                        if j!=len(M[0])-1:

                            dessine_ligne_entre(A(M, i, j), A(M, i, j + 1))

        dessine_lignes(M)
        dessine_les_points_de_la_matrice(M)

        def force_ressort(B,A,l,k): #force appliquée par le ressort se situant entre B et A sur A
            Ax = A[0]
            Ay = A[1]
            Bx = B[0]
            By = B[1]
            AB=np.sqrt((Bx - Ax) ** 2 + (By - Ay) ** 2)
            return [ k*(l - AB)*(Ax - Bx)/AB,  k * ((l/AB) - 1)*(Ay - By)/AB]

        def distance_entre(A,B):
            Ax = A[0]
            Ay = A[1]
            Bx = B[0]
            By = B[1]
            return(np.sqrt((Bx - Ax) ** 2 + (By - Ay) ** 2))

        for l in range(0,int(t*50/dt)):
            for i in range(0,len(M)):
                for j in range(0,len(M[0])):
                    if i==0:

                        if j==0:
                            F1 = force_ressort(A(M, i, j + 1), A(M, i, j), l, k)
                            F2 = force_ressort(A(M, i + 1, j), A(M, i, j), l, k)
                            F3 = force_ressort(A(M, i + 1, j + 1), A(M, i, j), d, k)
                            Fr = [F1[0] + F2[0] + F3[0], F1[1] + F2[1] + F3[1]]

                        if j!=0 and j!=len(M[0])-1:
                            F1 = force_ressort(A(M, i, j + 1), A(M, i, j), l, k)
                            F2 = force_ressort(A(M, i + 1, j), A(M, i, j), l, k)
                            F3 = force_ressort(A(M, i + 1, j + 1), A(M, i, j), d, k)
                            F4 = force_ressort(A(M, i, j - 1), A(M, i, j), l, k)
                            F5 = force_ressort(A(M, i + 1, j - 1), A(M, i, j), d, k)
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0], F1[1] + F2[1] + F3[1] + F4[1] + F5[1]]

                        if j==len(M[0])-1:
                            F2 = force_ressort(A(M, i + 1, j), A(M, i, j), l, k)
                            F4 = force_ressort(A(M, i, j - 1), A(M, i, j), l, k)
                            F5 = force_ressort(A(M, i + 1, j - 1), A(M, i, j), d, k)
                            Fr = [F4[0] + F2[0] + F5[0], F4[1] + F2[1] + F5[1]]

                    if i!=0 and i!=len(M)-1:

                        if j == 0:
                            F1 = force_ressort(A(M, i, j + 1), A(M, i, j), l, k)
                            F2 = force_ressort(A(M, i + 1, j), A(M, i, j), l, k)
                            F3 = force_ressort(A(M, i + 1, j + 1), A(M, i, j), d, k)
                            F6 = force_ressort(A(M, i - 1, j + 1), A(M, i, j), d, k)
                            F7 = force_ressort(A(M, i - 1, j), A(M, i, j), l, k)
                            Fr = [F1[0] + F2[0] + F3[0] + F6[0] + F7[0], F1[1] + F2[1] + F3[1] + F6[1] + F7[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(A(M, i, j + 1), A(M, i, j), l, k)
                            F2 = force_ressort(A(M, i + 1, j), A(M, i, j), l, k)
                            F3 = force_ressort(A(M, i + 1, j + 1), A(M, i, j), d, k)
                            F4 = force_ressort(A(M, i, j - 1), A(M, i, j), l, k)
                            F5 = force_ressort(A(M, i + 1, j - 1), A(M, i, j), d, k)
                            F6 = force_ressort(A(M, i - 1, j + 1), A(M, i, j), d, k)
                            F7 = force_ressort(A(M, i - 1, j), A(M, i, j), l, k)
                            F8 = force_ressort(A(M, i - 1, j - 1), A(M, i, j), d, k)
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0] + F6[0] + F7[0] + F8[0], F1[1] + F2[1] + F3[1] + F4[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F2 = force_ressort(A(M, i + 1, j), A(M, i, j), l, k)
                            F4 = force_ressort(A(M, i, j - 1), A(M, i, j), l, k)
                            F5 = force_ressort(A(M, i + 1, j - 1), A(M, i, j), d, k)
                            F7 = force_ressort(A(M, i - 1, j), A(M, i, j), l, k)
                            F8 = force_ressort(A(M, i - 1, j - 1), A(M, i, j), d, k)
                            Fr = [F4[0] + F2[0] + F5[0] + F7[0] + F8[0], F4[1] + F2[1] + F5[1] + F7[1] + F8[1]]

                    if i==len(M)-1:

                        if j == 0:
                            F1 = force_ressort(A(M, i, j + 1), A(M, i, j), l, k)
                            F6 = force_ressort(A(M, i - 1, j + 1), A(M, i, j), d, k)
                            F7 = force_ressort(A(M, i - 1, j), A(M, i, j), l, k)
                            Fr = [F1[0] + F6[0] + F7[0], F1[1] + F6[1] + F7[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(A(M, i, j + 1), A(M, i, j), l, k)
                            F4 = force_ressort(A(M, i, j - 1), A(M, i, j), l, k)
                            F6 = force_ressort(A(M, i - 1, j + 1), A(M, i, j), d, k)
                            F7 = force_ressort(A(M, i - 1, j), A(M, i, j), l, k)
                            F8 = force_ressort(A(M, i - 1, j - 1), A(M, i, j), d, k)
                            Fr = [F1[0] + F4[0] + F6[0] + F7[0] + F8[0], F1[1] + F4[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F4 = force_ressort(A(M, i, j - 1), A(M, i, j), l, k)
                            F7 = force_ressort(A(M, i - 1, j), A(M, i, j), l, k)
                            F8 = force_ressort(A(M, i - 1, j - 1), A(M, i, j), d, k)
                            Fr = [F4[0] + F7[0] + F8[0], F4[1] + F7[1] + F8[1]]

                    V[i][j] = [V[i][j][0] + (Fr[0] - alpha * V[i][j][0]) * dt / m, V[i][j][1] + (Fr[1] - alpha * V[i][j][1]) * dt / m]
                    M[i][j] = [M[i][j][0] + V[i][j][0] * dt, M[i][j][1] + V[i][j][1] * dt]

            canvas.delete("all")
            dessine_lignes(M)
            dessine_les_points_de_la_matrice(M)

            window.update()
            time.sleep(0.02 * dt)

        window.mainloop()

care=rectangle(0.1,10,10,[1,1],10,[1,1],[[0,0,1.05,0]],[0,0])
care.simuler(10,1/50,100)

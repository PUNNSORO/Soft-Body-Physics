import numpy as np
import time
from tkinter import *
import copy

#maintenant on commencera le codage de la simulation en 2D d'un objet rectangle à plusieurs particules qui sera defini
#simplement par les données de ses points qui se trouvent á ses extrimités, on commencera l'algorithme par implementer
#juste les forces de ressort et puis apres on definira les forces internes tq les forces inter particules qui aiderons
#á empecher l'objet de s'effondre sur lui meme, puis un peut plus tard on ajoutera les collisions qui rendrons la
#simulation plus reele, mais ce qui sera plus impressionnant est l'ajout des phase d'elasticité et de plasticité pour
#les materiaux, chose que je n'est pas encore y pensé une solution mais on vera!!!

def matrice(y,x):
     F=[]
     for k in range(0,y):
        L=[]
        for l in range(0,x):
            s='.'
            L.append(s)
        F.append(L)
     return F

class rectangle:
    def __init__(self,longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotation):
        self.len = longueur_precision_spaciale
        self.stif = raideur
        self.dissip = dissipation_lors_des_collision
        self.dim = dimensions
        self.mass = mass
        self.position = position_initial
        self.start = positions_de_qlq_points
        self.alpha = alpha
        self.vit = vitesse_de_G
        self.rot = rotation

    def simuler(self,temps_de_la_simulation,precision_dt,scale):
        t = temps_de_la_simulation
        dt = precision_dt
        s=scale
        epsilon = 4*0.25/100

        LIST_deformation = []
        for i in range(0, 46):
            LIST_deformation.append(epsilon)

        contrainte = [0, 14.5, 29, 37, 38, 38.5, 39, 39.5, 39.75, 40, 40.4, 40.6, 40.8, 41, 41.2, 41.4, 41.6, 41.8,
                      41.98, 42.16, 42.34, 42.42, 42.6, 42.75, 42.88
            , 43, 43.1, 43.2, 43.3, 43.4, 43.45, 43.49, 43.53, 43.575, 43.6, 43.65, 43.7, 43.7, 43.7, 43.7, 43.7, 43.65,
                      43.4, 43, 42.5, 42]

        for i in range(0,len(contrainte)):
            contrainte[i] = contrainte[i] * 0.1

        young_init = contrainte[1]/LIST_deformation[1]
        k = 500

        alpha = self.alpha
        l = self.len
        d = l*np.sqrt(3)
        dissip = self.dissip
        a = np.floor(self.dim[0]/l)*l
        b = np.floor(self.dim[1]/l)*l
        c = np.floor(self.dim[2]/l)*l
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        g = 9.81
        omega = self.rot

        #M est la matrice representant les points du solide

        def distance_entre(B, A):
            Ax = A[0]
            Ay = A[1]
            Az = A[2]
            Bx = B[0]
            By = B[1]
            Bz = B[2]
            return np.sqrt((Bx - Ax) ** 2 + (By - Ay) ** 2 + (Bz - Az) ** 2)


        def force_ressort(B, A, l, k):  # force appliquée par le ressort se situant entre B et A sur A
            Ax = A[0]
            Ay = A[1]
            Az = A[2]
            Bx = B[0]
            By = B[1]
            Bz = B[2]
            AB = distance_entre(B, A)
            return [k * (l - AB) * (Ax - Bx) / AB, k * (l - AB) * (Ay - By) / AB, k * (l - AB) * (Az - Bz) / AB]

        M = []
        V = []
        ACC = []
        F = []
        liaisons = []
        nombre_de_points=0

        for i in range(0,int(b/l)):
            L=[]
            K=[]
            I=[]
            T=[]
            liaisons_1er_coor_1er_pts = []

            for j in range(0,int(a/l)):
                list_des_points = []
                list_des_vitesses = []
                list_des_acc = []
                list_des_forces = []
                liaisons_2eme_coor_1er_pts = []

                for ka in range(0,int(c/l)):
                    nombre_de_points += 1
                    list_des_points.append([x + l * j, y + l * i, z + l * ka - 9])
                    list_des_vitesses.append(self.vit)
                    list_des_acc.append([0, 0, 0])
                    list_des_forces.append([0, 0, 0])
                    liaisons_3eme_coor_1er_pts = []

                    for u in range(0, int(b / l)):
                        liaisons_1er_coor_2eme_pts = []
                        for z in range(0, int(a / l)):
                            liaisons_2eme_coor_2eme_pts = []
                            for o in range(0, int(c / l)):
                                liaisons_3eme_coor_2eme_pts = 0
                                liaisons_2eme_coor_2eme_pts.append(liaisons_3eme_coor_2eme_pts)
                            liaisons_1er_coor_2eme_pts.append(liaisons_2eme_coor_2eme_pts)
                        liaisons_3eme_coor_1er_pts.append(liaisons_1er_coor_2eme_pts)
                    liaisons_2eme_coor_1er_pts.append(liaisons_3eme_coor_1er_pts)

                L.append(list_des_points)
                K.append(list_des_vitesses)
                I.append(list_des_acc)
                T.append(list_des_forces)
                liaisons_1er_coor_1er_pts.append(liaisons_2eme_coor_1er_pts)

            liaisons.append(liaisons_1er_coor_1er_pts)
            M.append(L)
            V.append(K)
            ACC.append(I)
            F.append(T)

        M[0][0][0][2] = 0

        print(M)


        alpha = alpha/nombre_de_points

        for i in range(0, len(M)):
            for j in range(0, len(M[0])):
                for ka in range(0, len(M[0][0])):
                    if i == 0:

                        if j == 0:

                            if ka == 0:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i + 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 22

                            if ka != 0 and ka != len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i + 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 22
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i + 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 32

                            if ka == len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i + 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 32

                        if j != 0 and j != len(M[0]) - 1:

                            if ka == 0:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i + 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 22
                                liaisons[i][j][ka][i + 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 25

                            if ka != 0 and ka != len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i + 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 22
                                liaisons[i][j][ka][i + 1][j - 1][ka + 1] = [d,k,[contrainte,LIST_deformation],d,d] # 25
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i + 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 32
                                liaisons[i][j][ka][i + 1][j - 1][ka - 1] = [d,k,[contrainte,LIST_deformation],d,d] # 35

                            if ka == len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i + 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 32
                                liaisons[i][j][ka][i + 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 35

                        if j == len(M[0]) - 1:
                            if ka == 0:
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i + 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 25

                            if ka != 0 and ka != len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i + 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 25
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i + 1][j - 1][ka - 1] = [d,k,[contrainte,LIST_deformation],d,d] # 35

                            if ka == len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i + 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 35

                    if i != 0 and i != len(M) - 1:

                        if j == 0:
                            if ka == 0:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i + 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 22
                                liaisons[i][j][ka][i - 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 23

                            if ka != 0 and ka != len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i + 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 22
                                liaisons[i][j][ka][i - 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 23
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i + 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 32
                                liaisons[i][j][ka][i - 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 33

                            if ka == len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i + 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 32
                                liaisons[i][j][ka][i - 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 33

                        if j != 0 and j != len(M[0]) - 1:
                            if ka == 0:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i + 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 22
                                liaisons[i][j][ka][i - 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 23
                                liaisons[i][j][ka][i - 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 24
                                liaisons[i][j][ka][i + 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 25

                            if ka != 0 and ka != len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l,k,[contrainte,LIST_deformation],l,l] # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l,k,[contrainte,LIST_deformation],l,l] # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l,k,[contrainte,LIST_deformation],l,l] # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l,k,[contrainte,LIST_deformation],l,l] # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l,k,[contrainte,LIST_deformation],l,l] # 21
                                liaisons[i][j][ka][i + 1][j + 1][ka + 1] = [d,k,[contrainte,LIST_deformation],d,d] # 22
                                liaisons[i][j][ka][i - 1][j + 1][ka + 1] = [d,k,[contrainte,LIST_deformation],d,d] # 23
                                liaisons[i][j][ka][i - 1][j - 1][ka + 1] = [d,k,[contrainte,LIST_deformation],d,d] # 24
                                liaisons[i][j][ka][i + 1][j - 1][ka + 1] = [d,k,[contrainte,LIST_deformation],d,d] # 25
                                liaisons[i][j][ka][i][j][ka - 1] = [l,k,[contrainte,LIST_deformation],l,l] # 31
                                liaisons[i][j][ka][i + 1][j + 1][ka - 1] = [d,k,[contrainte,LIST_deformation],d,d] # 32
                                liaisons[i][j][ka][i - 1][j + 1][ka - 1] = [d,k,[contrainte,LIST_deformation],d,d] # 33
                                liaisons[i][j][ka][i - 1][j - 1][ka - 1] = [d,k,[contrainte,LIST_deformation],d,d] # 34
                                liaisons[i][j][ka][i + 1][j - 1][ka - 1] = [d,k,[contrainte,LIST_deformation],d,d] # 35

                            if ka == len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i + 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 32
                                liaisons[i][j][ka][i - 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 33
                                liaisons[i][j][ka][i - 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 34
                                liaisons[i][j][ka][i + 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 35

                        if j == len(M[0]) - 1:
                            if ka == 0:
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l,k,[contrainte,LIST_deformation],l,l]  # 21
                                liaisons[i][j][ka][i - 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 24
                                liaisons[i][j][ka][i + 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 25

                            if ka != 0 and ka != len(M[0][0]) - 1:
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i - 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 24
                                liaisons[i][j][ka][i + 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 25
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i - 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 34
                                liaisons[i][j][ka][i + 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 35

                            if ka == len(M[0][0]) - 1:
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i + 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 14
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i - 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 34
                                liaisons[i][j][ka][i + 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 35

                    if i == len(M) - 1:

                        if j == 0:

                            if ka == 0:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i - 1][j + 1][ka + 1] = [d,k,[contrainte,LIST_deformation],d,d] # 23

                            if ka != 0 and ka != len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i - 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 23
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i - 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 33

                            if ka == len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i - 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 33

                        if j != 0 and j != len(M[0]) - 1:
                            if ka == 0:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i - 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 23
                                liaisons[i][j][ka][i - 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 24

                            if ka != 0 and ka != len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i - 1][j + 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 23
                                liaisons[i][j][ka][i - 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 24
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i - 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 33
                                liaisons[i][j][ka][i - 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 34

                            if ka == len(M[0][0]) - 1:
                                liaisons[i][j][ka][i][j + 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 11
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i - 1][j + 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 33
                                liaisons[i][j][ka][i - 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 34

                        if j == len(M[0]) - 1:

                            if ka == 0:
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i - 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 24

                            if ka != 0 and ka != len(M[0][0]) - 1:
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i][j][ka + 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 21
                                liaisons[i][j][ka][i - 1][j - 1][ka + 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 24
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i - 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 34

                            if ka == len(M[0][0]) - 1:
                                liaisons[i][j][ka][i - 1][j][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 12
                                liaisons[i][j][ka][i][j - 1][ka] = [l, k, [contrainte, LIST_deformation], l, l]  # 13
                                liaisons[i][j][ka][i][j][ka - 1] = [l, k, [contrainte, LIST_deformation], l, l]  # 31
                                liaisons[i][j][ka][i - 1][j - 1][ka - 1] = [d, k, [contrainte, LIST_deformation], d,
                                                                            d]  # 34


        liaisons_initiales = copy.deepcopy(liaisons)

        def deformation_calculation(Bi, Bj, Ai, Aj):
            epsilon = (distance_entre(M[Ai][Aj], M[Bi][Bj])-liaisons[Ai][Aj][Bi][Bj][0])/liaisons[Ai][Aj][Bi][Bj][0]

            return epsilon

        def young(Bi, Bj, Ai, Aj):
            if liaisons[Ai][Aj][Bi][Bj][1] != 0:
                defor = deformation_calculation(Bi, Bj, Ai, Aj)
                if defor > 0 :
                    if defor >= liaisons[Ai][Aj][Bi][Bj][2][1][len(liaisons[Ai][Aj][Bi][Bj][2][1]) - 1]:
                        return 0
                    else:
                        if defor <= liaisons[Ai][Aj][Bi][Bj][2][1][1] :
                            return young_init
                        else:
                            indice = int(1 + np.floor((defor - liaisons[Ai][Aj][Bi][Bj][2][1][1]) / LIST_deformation[1]))
                            return (liaisons[Ai][Aj][Bi][Bj][2][0][indice + 1] - liaisons[Ai][Aj][Bi][Bj][2][0][indice]) / LIST_deformation[1]

                if defor <= 0:
                    return k

            if liaisons[Ai][Aj][Bi][Bj][1] == 0:
                return 0

        def raideur(Bi, Bj, Ai, Aj):
            return young(Bi, Bj, Ai, Aj)

        def update_raideur(Bi, Bj, Ai, Aj):

            deformation_t = deformation_calculation(Bi, Bj, Ai, Aj)
            new_distance = distance_entre(M[Ai][Aj], M[Bi][Bj])
            old_distance = liaisons[Ai][Aj][Bi][Bj][4]
            Deformation = liaisons[Ai][Aj][Bi][Bj][2][1]
            Contrainte = liaisons[Ai][Aj][Bi][Bj][2][0]
            distance_initial = liaisons[Ai][Aj][Bi][Bj][3]

            N = len(Contrainte)
            indice_de_deformation = int(1 + np.abs(np.floor((deformation_t - Deformation[1]) / LIST_deformation[1])))
            new_raideur = k
            if new_distance < old_distance and new_distance > distance_initial :
                if indice_de_deformation >0 and indice_de_deformation < N-1:
                    print(11)
                    new_length = new_distance
                    if new_length <= liaisons[Ai][Aj][Bi][Bj][0]:
                        new_length = liaisons[Ai][Aj][Bi][Bj][0]

                    Contrainte = Contrainte[indice_de_deformation::]
                    Deformation = Deformation[indice_de_deformation::]
                    Contrainte[0] = 0

                    delta_deformation = (Contrainte[1]) / k
                    Deformation[0] = 0
                    Deformation[1] = delta_deformation

                    for j in range(2, len(Deformation)):
                        Deformation[j] = (j - 1) * 0.25 / 100 + delta_deformation

                    return [new_length, new_raideur, [Contrainte, Deformation], distance_initial, new_distance]

                if indice_de_deformation == 0 :
                    return liaisons[Ai][Aj][Bi][Bj]

                else:
                    [liaisons[Ai][Aj][Bi][Bj][0], 0, [liaisons[Ai][Aj][Bi][Bj][2][0], liaisons[Ai][Aj][Bi][Bj][2][1]]]

            if new_distance >= old_distance:
                if deformation_t > Deformation[len(Deformation)-1] :
                    return [liaisons[Ai][Aj][Bi][Bj][0], 0, [liaisons[Ai][Aj][Bi][Bj][2][0], liaisons[Ai][Aj][Bi][Bj][2][1]]]
                else:
                    return [liaisons[Ai][Aj][Bi][Bj][0], new_raideur, [liaisons[Ai][Aj][Bi][Bj][2][0], liaisons[Ai][Aj][Bi][Bj][2][1]], liaisons[Ai][Aj][Bi][Bj][3], new_distance]


            else:
                return [liaisons[Ai][Aj][Bi][Bj][0], liaisons[Ai][Aj][Bi][Bj][1], [liaisons[Ai][Aj][Bi][Bj][2][0], liaisons[Ai][Aj][Bi][Bj][2][1]], liaisons[Ai][Aj][Bi][Bj][3], new_distance]

        m = self.mass/nombre_de_points

        poids = -m*g*1

        #maintenant on reorganise quelque points suivant les commande de positions_de_qlq_points

        for o in self.start:
            i=o[0]
            j=o[1]
            ka=o[2]
            M[i][j][ka]=[M[i][j][ka][0]+o[3]*l, M[i][j][ka][1]+o[4]*l, M[i][j][ka][2]+o[5]*l]

        W = 800
        H = 650
        window = Tk()
        canvas = Canvas(window, width=W, height=H, bg="white")
        canvas.pack()

        def A(L, i, j, ka):  # une fonction qui aidera á bien organiser les points de la matrice
            return [L[i][j][ka][0] + 0.25 * L[i][j][ka][2], L[i][j][ka][1] + 0.4 * L[i][j][ka][2]]

        def dessine_point(A):
            size = 4
            canvas.create_oval(A[0] * s - size, H - A[1] * s + size, A[0] * s + size, H - A[1] * s - size, fill="black")

        def dessine_les_points_de_la_matrice(M):
            for i in range(0, len(M)):
                for j in range(0, len(M[0])):
                    for ka in range(0, len(M[0][0])):
                        dessine_point(A(M, i, j, ka))

        def dessine_ligne_entre(A, B):
            C = [0, 0]
            D = [0, 0]
            C[0] = A[0] + 0.25 * A[2]
            C[1] = A[1] + 0.4 * A[2]
            D[0] = B[0] + 0.25 * B[2]
            D[1] = B[1] + 0.4 * B[2]
            canvas.create_line(C[0] * s, H - C[1] * s, D[0] * s, H - D[1] * s, fill="red")

        def pivoter_point(A,B,phi):
            return [np.cos(phi)*(A[0]-B[0])-np.sin(phi)*(A[1]-B[1])+B[0],np.cos(phi)*(A[1]-B[1])+np.sin(phi)*(A[0]-B[0])+B[1]]

        def pivoter_rectangle(M,B,phi):
            for i in range(0,len(M)):
                for j in range(0,len(M[0])):
                    M[i][j]=pivoter_point(M[i][j],B,phi)

        def dessine_lignes(M):
            for i in range(0, len(M)):
                for j in range(0, len(M[0])):
                    for ka in range(0, len(M[0][0])):
                        if i == 0:

                            if j == 0:

                                if ka == 0:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])


                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                                if ka == len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                            if j != 0 and j != len(M[0]) - 1:

                                if ka == 0:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                                if ka == len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                            if j == len(M[0]) - 1:
                                if ka == 0:
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                                if ka == len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                        if i != 0 and i != len(M) - 1:

                            if j == 0:
                                if ka == 0:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])

                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                                if ka == len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                            if j != 0 and j != len(M[0]) - 1:
                                if ka == 0:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                                if ka == len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                            if j == len(M[0]) - 1:
                                if ka == 0:
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                                if ka == len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i + 1][j][ka][1] != 0:  # 14
                                        dessine_ligne_entre(M[i + 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                        if i == len(M) - 1:

                            if j == 0:

                                if ka == 0:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                                if ka == len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                            if j != 0 and j != len(M[0]) - 1:
                                if ka == 0:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                                if ka == len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i][j + 1][ka][1] != 0:  # 11
                                        dessine_ligne_entre(M[i][j + 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                            if j == len(M[0]) - 1:

                                if ka == 0:
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka + 1][1] != 0:  # 21
                                        dessine_ligne_entre(M[i][j][ka + 1], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

                                if ka == len(M[0][0]) - 1:
                                    if liaisons[i][j][ka][i - 1][j][ka][1] != 0:  # 12
                                        dessine_ligne_entre(M[i - 1][j][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j - 1][ka][1] != 0:  # 13
                                        dessine_ligne_entre(M[i][j - 1][ka], M[i][j][ka])
                                    if liaisons[i][j][ka][i][j][ka - 1][1] != 0:  # 31
                                        dessine_ligne_entre(M[i][j][ka - 1], M[i][j][ka])

        def update_les_ressort(M):
            for i in range(0, len(M)):
                for j in range(0, len(M[0])):

                    if i != len(M) - 1:

                        if j == 0:
                            if liaisons[i][j][i + 1][j][1] != 0:
                                place_holder = update_raideur(i, j, i + 1, j)
                                liaisons[i][j][i + 1][j] = place_holder
                                liaisons[i + 1][j][i][j] = place_holder
                            if liaisons[i][j][i][j + 1][1] != 0:
                                place_holder = update_raideur(i, j, i, j + 1)
                                liaisons[i][j][i][j + 1] = place_holder
                                liaisons[i][j + 1][i][j] = place_holder
                            if liaisons[i][j][i + 1][j + 1][1] != 0:
                                place_holder = update_raideur( i, j, i + 1, j + 1)
                                liaisons[i][j][i + 1][j + 1] = place_holder
                                liaisons[i + 1][j + 1][i][j] = place_holder

                        if j != 0 and j != len(M[0]) - 1:
                            if liaisons[i][j][i + 1][j][1] != 0:
                                place_holder = update_raideur(i, j, i + 1, j)
                                liaisons[i][j][i + 1][j] = place_holder
                                liaisons[i + 1][j][i][j] = place_holder
                            if liaisons[i][j][i][j + 1][1] != 0:
                                place_holder = update_raideur(i, j, i, j + 1)
                                liaisons[i][j][i][j + 1] = place_holder
                                liaisons[i][j + 1][i][j] = place_holder
                            if liaisons[i][j][i + 1][j + 1][1] != 0:
                                place_holder = update_raideur(i, j, i + 1, j + 1)
                                liaisons[i][j][i + 1][j + 1] = place_holder
                                liaisons[i + 1][j + 1][i][j] = place_holder
                            if liaisons[i][j][i + 1][j - 1][1] != 0:
                                place_holder = update_raideur( i, j, i + 1, j - 1)
                                liaisons[i][j][i + 1][j - 1] = place_holder
                                liaisons[i + 1][j - 1][i][j] = place_holder

                        if j == len(M[0]) - 1:
                            if liaisons[i][j][i + 1][j][1] != 0:
                                place_holder = update_raideur(i, j, i + 1, j)
                                liaisons[i][j][i + 1][j] = place_holder
                                liaisons[i + 1][j][i][j] = place_holder
                            if liaisons[i][j][i + 1][j - 1][1] != 0:
                                place_holder = update_raideur(i, j, i + 1, j - 1)
                                liaisons[i][j][i + 1][j - 1] = place_holder
                                liaisons[i + 1][j - 1][i][j] = place_holder

                    if i == len(M) - 1:
                        if j != len(M[0]) - 1:
                            if liaisons[i][j][i][j + 1][1] != 0:
                                place_holder = update_raideur(i, j, i, j + 1)
                                liaisons[i][j][i][j + 1] = place_holder
                                liaisons[i][j + 1][i][j] = place_holder

        def calculer_force(F11, F12, F13, F14, F21, F22, F23, F24, F25, F31, F32, F33, F34, F35):

            LIST_FORCES = [F11, F12, F13, F14, F21, F22, F23, F24, F25, F31, F32, F33, F34, F35]
            Fr = [0, 0, 0]
            for i in LIST_FORCES:

                if i != None:
                    Fr = [Fr[0] + i[0], Fr[1] + i[1], Fr[2] + i[2]]

                else :
                    Fr = [Fr[0] + 0, Fr[1] + 0, Fr[2] + 0]

            return Fr


        # pivoter_rectangle(M,M[0][0],omega)
        dessine_lignes(M)
        dessine_les_points_de_la_matrice(M)

        fixer_1er_ligne_y = 1  # 0 pour non 1 pour oui
        fixer_dernier_ligne_y = 1  # 0 pour non 1 pour oui
        fixer_1er_ligne_x = 0  # 0 pour non 1 pour oui
        duree_de_force = 150

        number_of_frames=0

        def calculer_forces(M):
            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0]) - fixer_dernier_ligne_y):
                    for ka in range(0, len(M[0][0])):
                        # F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka], liaisons[i][j][ka][i][j + 1][ka][0],
                        #                     liaisons[i][j][ka][i][j + 1][ka][1])
                        # F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka], liaisons[i][j][ka][i - 1][j][ka][0],
                        #                     liaisons[i][j][ka][i - 1][j][ka][1])
                        # F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka], liaisons[i][j][ka][i][j - 1][ka][0],
                        #                     liaisons[i][j][ka][i][j - 1][ka][1])
                        # F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka], liaisons[i][j][ka][i + 1][j][ka][0],
                        #                     liaisons[i][j][ka][i + 1][j][ka][1])
                        #
                        # F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka], liaisons[i][j][ka][i][j][ka + 1][0],
                        #                     liaisons[i][j][ka][i][j][ka + 1][1])
                        # F22 = force_ressort(M[i + 1][j + 1][ka + 1], M[i][j][ka],
                        #                     liaisons[i][j][ka][i + 1][j + 1][ka + 1][0],
                        #                     liaisons[i][j][ka][i + 1][j + 1][ka + 1][1])
                        # F23 = force_ressort(M[i - 1][j + 1][ka + 1], M[i][j][ka],
                        #                     liaisons[i][j][ka][i - 1][j + 1][ka + 1][0],
                        #                     liaisons[i][j][ka][i - 1][j + 1][ka + 1][1])
                        # F24 = force_ressort(M[i - 1][j - 1][ka + 1], M[i][j][ka],
                        #                     liaisons[i][j][ka][i - 1][j - 1][ka + 1][0],
                        #                     liaisons[i][j][ka][i - 1][j - 1][ka + 1][1])
                        # F25 = force_ressort(M[i + 1][j - 1][ka + 1], M[i][j][ka],
                        #                     liaisons[i][j][ka][i + 1][j - 1][ka + 1][0],
                        #                     liaisons[i][j][ka][i + 1][j - 1][ka + 1][1])
                        #
                        # F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka], liaisons[i][j][ka][i][j][ka - 1][0],
                        #                     liaisons[i][j][ka][i][j][ka - 1][1])
                        # F32 = force_ressort(M[i + 1][j + 1][ka - 1], M[i][j][ka],
                        #                     liaisons[i][j][ka][i + 1][j + 1][ka - 1][0],
                        #                     liaisons[i][j][ka][i + 1][j + 1][ka - 1][1])
                        # F33 = force_ressort(M[i - 1][j + 1][ka - 1], M[i][j][ka],
                        #                     liaisons[i][j][ka][i - 1][j + 1][ka - 1][0],
                        #                     liaisons[i][j][ka][i - 1][j + 1][ka - 1][1])
                        # F34 = force_ressort(M[i - 1][j - 1][ka - 1], M[i][j][ka],
                        #                     liaisons[i][j][ka][i - 1][j - 1][ka - 1][0],
                        #                     liaisons[i][j][ka][i - 1][j - 1][ka - 1][1])
                        # F35 = force_ressort(M[i + 1][j - 1][ka - 1], M[i][j][ka],
                        #                     liaisons[i][j][ka][i + 1][j - 1][ka - 1][0],
                        #                     liaisons[i][j][ka][i + 1][j - 1][ka - 1][1])

                        if i == 0:

                            if j == 0:

                                if ka == 0:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])
                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F22 = force_ressort(M[i + 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][1])

                                    Fr = calculer_force(F11, None, None, F14, F21, F22, None, None, None, None, None, None, None, None)


                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])
                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F22 = force_ressort(M[i + 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][1])
                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F32 = force_ressort(M[i + 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][1])
                                    Fr = calculer_force(F11, None, None, F14, F21, F22, None, None, None, F31, F32, None, None, None)

                                if ka == len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])
                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F32 = force_ressort(M[i + 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][1])
                                    Fr = calculer_force(F11, None, None, F14, None, None, None, None, None, F31, F32, None, None, None)



                            if j != 0 and j != len(M[0]) - 1:

                                if ka == 0:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])
                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F22 = force_ressort(M[i + 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][1])
                                    F25 = force_ressort(M[i + 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][1])
                                    Fr = calculer_force(F11, None, F13, F14, F21, F22, None, None, F25, None, None, None, None, None)


                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])
                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F22 = force_ressort(M[i + 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][1])
                                    F25 = force_ressort(M[i + 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][1])
                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F32 = force_ressort(M[i + 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][1])
                                    F35 = force_ressort(M[i + 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(F11, None, F13, F14, F21, F22, None, None, F25, F31, F32, None, None, F35)

                                if ka == len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])
                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F32 = force_ressort(M[i + 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][1])
                                    F35 = force_ressort(M[i + 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(F11, None, F13, F14, None, None, None, None, None, F31, F32, None, None, F35)


                            if j == len(M[0]) - 1:
                                if ka == 0:
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])
                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F25 = force_ressort(M[i + 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][1])
                                    Fr = calculer_force(None, None, F13, F14, F21, None, None, None, F25, None, None, None, None, None)

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])
                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F25 = force_ressort(M[i + 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][1])
                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F35 = force_ressort(M[i + 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(None, None, F13, F14, F21, None, None, None, F25, F31, None, None, None, F35)

                                if ka == len(M[0][0]) - 1:
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])
                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F35 = force_ressort(M[i + 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(None, None, F13, F14, None, None, None, None, None, F31, None, None, None, F35)

                        if i != 0 and i != len(M) - 1:

                            if j == 0:
                                if ka == 0:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F22 = force_ressort(M[i + 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][1])
                                    F23 = force_ressort(M[i - 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][1])
                                    Fr = calculer_force(F11, F12, None, F14, F21, F22, F23, None, None, None, None, None, None, None)


                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F22 = force_ressort(M[i + 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][1])
                                    F23 = force_ressort(M[i - 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F32 = force_ressort(M[i + 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][1])
                                    F33 = force_ressort(M[i - 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][1])
                                    Fr = calculer_force(F11, F12, None, F14, F21, F22, F23, None, None, F31, F32, F33, None, None)


                                if ka == len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F32 = force_ressort(M[i + 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][1])
                                    F33 = force_ressort(M[i - 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][1])
                                    Fr = calculer_force(F11, F12, None, F14, None, None, None, None, None, F31, F32, F33, None, None)

                            if j != 0 and j != len(M[0]) - 1:
                                if ka == 0:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F22 = force_ressort(M[i + 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][1])
                                    F23 = force_ressort(M[i - 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][1])
                                    F24 = force_ressort(M[i - 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][1])
                                    F25 = force_ressort(M[i + 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][1])
                                    Fr = calculer_force(F11, F12, F13, F14, F21, F22, F23, F24, F25, None, None, None, None, None)


                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F22 = force_ressort(M[i + 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka + 1][1])
                                    F23 = force_ressort(M[i - 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][1])
                                    F24 = force_ressort(M[i - 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][1])
                                    F25 = force_ressort(M[i + 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F32 = force_ressort(M[i + 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][1])
                                    F33 = force_ressort(M[i - 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][1])
                                    F34 = force_ressort(M[i - 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][1])
                                    F35 = force_ressort(M[i + 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(F11, F12, F13, F14, F21, F22, F23, F24, F25, F31, F32, F33, F34, F35)

                                if ka == len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F32 = force_ressort(M[i + 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j + 1][ka - 1][1])
                                    F33 = force_ressort(M[i - 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][1])
                                    F34 = force_ressort(M[i - 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][1])
                                    F35 = force_ressort(M[i + 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(F11, F12, F13, F14, None, None, None, None, None, F31, F32, F33, F34, F35)



                            if j == len(M[0]) - 1:
                                if ka == 0:
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F24 = force_ressort(M[i - 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][1])
                                    F25 = force_ressort(M[i + 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][1])
                                    Fr = calculer_force(None, F12, F13, F14, F21, None, None, F24, F25, None, None, None, None, None)

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F24 = force_ressort(M[i - 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][1])
                                    F25 = force_ressort(M[i + 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka + 1][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F34 = force_ressort(M[i - 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][1])
                                    F35 = force_ressort(M[i + 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(None, F12, F13, F14, F21, None, None, F24, F25, F31, None, None, F34, F35)

                                if ka == len(M[0][0]) - 1:
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F14 = force_ressort(M[i + 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j][ka][0],
                                                        liaisons[i][j][ka][i + 1][j][ka][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F34 = force_ressort(M[i - 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][1])
                                    F35 = force_ressort(M[i + 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i + 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(None, F12, F13, F14, None, None, None, None, None, F31, None, None, F34, F35)

                        if i == len(M) - 1:

                            if j == 0:

                                if ka == 0:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F23 = force_ressort(M[i - 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][1])
                                    Fr = calculer_force(F11, F12, None, None, F21, None, F23, None, None, None, None, None, None, None)

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F23 = force_ressort(M[i - 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F33 = force_ressort(M[i - 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][1])
                                    Fr = calculer_force(F11, F12, None, None, F21, None, F23, None, None, F31, None, F33, None, None)

                                if ka == len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F33 = force_ressort(M[i - 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][1])
                                    Fr = calculer_force(F11, F12, None, None, None, None, None, None, None, F31, None, F33, None, None)

                            if j != 0 and j != len(M[0]) - 1:
                                if ka == 0:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F23 = force_ressort(M[i - 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][1])
                                    F24 = force_ressort(M[i - 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][1])
                                    Fr = calculer_force(F11, F12, F13, None, F21, None, F23, F24, None, None, None, None, None, None)

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F23 = force_ressort(M[i - 1][j + 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka + 1][1])
                                    F24 = force_ressort(M[i - 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F33 = force_ressort(M[i - 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][1])
                                    F34 = force_ressort(M[i - 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(F11, F12, F13, None, F21, None, F23, F24, None, F31, None, F33, F34, None)

                                if ka == len(M[0][0]) - 1:
                                    F11 = force_ressort(M[i][j + 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j + 1][ka][0],
                                                        liaisons[i][j][ka][i][j + 1][ka][1])
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F33 = force_ressort(M[i - 1][j + 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j + 1][ka - 1][1])
                                    F34 = force_ressort(M[i - 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(F11, F12, F13, None, None, None, None, None, None, F31, None, F33, F34, None)



                            if j == len(M[0]) - 1:

                                if ka == 0:
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F24 = force_ressort(M[i - 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][1])
                                    Fr = calculer_force(None, F12, F13, None, F21, None, None, F24, None, None, None, None, None, None)

                                if ka != 0 and ka != len(M[0][0]) - 1:
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])

                                    F21 = force_ressort(M[i][j][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka + 1][0],
                                                        liaisons[i][j][ka][i][j][ka + 1][1])
                                    F24 = force_ressort(M[i - 1][j - 1][ka + 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka + 1][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F34 = force_ressort(M[i - 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(None, F12, F13, None, F21, None, None, F24, None, F31, None, None, F34, None)

                                if ka == len(M[0][0]) - 1:
                                    F13 = force_ressort(M[i][j - 1][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j - 1][ka][0],
                                                        liaisons[i][j][ka][i][j - 1][ka][1])
                                    F12 = force_ressort(M[i - 1][j][ka], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j][ka][0],
                                                        liaisons[i][j][ka][i - 1][j][ka][1])

                                    F31 = force_ressort(M[i][j][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i][j][ka - 1][0],
                                                        liaisons[i][j][ka][i][j][ka - 1][1])
                                    F34 = force_ressort(M[i - 1][j - 1][ka - 1], M[i][j][ka],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][0],
                                                        liaisons[i][j][ka][i - 1][j - 1][ka - 1][1])
                                    Fr = calculer_force(None, F12, F13, None, None, None, None, None, None, F31, None, None, F34, None)

                        F[i][j][ka] = Fr

        def calculer_position(M,q):
            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0]) - fixer_dernier_ligne_y):
                    for ka in range(0, len(M[0][0])):

                        if i == 1 and j == np.floor(len(M[0]) - 1) and q < duree_de_force:
                            force_horizontale = 0
                            force_verticale = 0


                        else:
                            force_horizontale = 0
                            force_verticale = 0



                        ACC[i][j][ka][0] = (F[i][j][ka][0] - alpha * V[i][j][ka][0] + force_horizontale) / m
                        ACC[i][j][ka][1] = (F[i][j][ka][1] - alpha * V[i][j][ka][1] + poids + force_verticale) / m
                        ACC[i][j][ka][2] = (F[i][j][ka][2] - alpha * V[i][j][ka][2] ) / m *0

                        M[i][j][ka][0] = M[i][j][ka][0] + V[i][j][ka][0] * dt + dt ** 2 / 2 * ACC[i][j][ka][0]
                        M[i][j][ka][1] = M[i][j][ka][1] + V[i][j][ka][1] * dt + dt ** 2 / 2 * ACC[i][j][ka][1]
                        M[i][j][ka][2] = M[i][j][ka][2] + V[i][j][ka][2] * dt + dt ** 2 / 2 * ACC[i][j][ka][2]


        def calculer_vitesse(M):
            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0])-fixer_dernier_ligne_y):
                    if  j == len(M[0]) - 1 and q < duree_de_force:
                        force_horizontale = 0
                        force_verticale = 0

                    else:
                        force_horizontale = 0
                        force_verticale = 0

                    acc_Aij_x_1 = (F[i][j][ka][0] - alpha * V[i][j][ka][0] + force_horizontale) / m
                    acc_Aij_y_1 = (F[i][j][ka][1] - alpha * V[i][j][ka][1] + poids + force_verticale) / m
                    acc_Aij_z_1 = (F[i][j][ka][2] - alpha * V[i][j][ka][2]) / m *0

                    acc_Aij_x_0 = ACC[i][j][ka][0]
                    acc_Aij_y_0 = ACC[i][j][ka][1]
                    acc_Aij_z_0 = ACC[i][j][ka][2]

                    V[i][j][ka][0] = V[i][j][ka][0] + dt / 2 * (acc_Aij_x_1 + acc_Aij_x_0)
                    V[i][j][ka][1] = V[i][j][ka][1] + dt / 2 * (acc_Aij_y_1 + acc_Aij_y_0)
                    V[i][j][ka][2] = V[i][j][ka][2] + dt / 2 * (acc_Aij_z_1 + acc_Aij_z_0)


                    if M[i][j][ka][0]<0: #les collisions avec le sol et les murs

                        M[i][j][ka][0] = 0
                        V[i][j][ka][0] = -V[i][j][ka][0]*dissip

                    if M[i][j][ka][1]<0:

                        M[i][j][ka][1] = 0
                        V[i][j][ka][1] = -V[i][j][ka][1]*dissip

        for q in range(0,int(t/dt)):
            start_time=time.time()

            calculer_forces(M)

            calculer_position(M, q)

            # update_les_ressort(M)

            calculer_forces(M)

            calculer_vitesse(M)


            end_time=time.time()

            frame_calculation_time=end_time-start_time

            canvas.delete("all")
            dessine_lignes(M)
            dessine_les_points_de_la_matrice(M)


            number_of_frames+=1
            print(number_of_frames*dt,"-------",q)


            window.update()

        window.mainloop()

# care=rectangle(1/10,1000,0.5,1,[1,0.2],1,[0.2,1],[[0,0,0,0]],[0,0],np.pi/6) #longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/300,300)#temps_de_la_simulation,precision_dt,scale

care=rectangle(1/5,50,0.5,200,[2,0.7,0.7],10,[0.1,1,-9],[[0,0,0,0,0,0]],[0,0,0],np.pi * 0)#longueur, raideur, dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
care.simuler(10000,1/(600*1),200)#temps_de_la_simulation,precision_dt,scale

# care=rectangle(1/20,25,0.5,0.2,[0.1,0.1],1,[0.1,0.1],[[0,0,0,0]],[0,0],0)#longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/5000,2000)#temps_de_la_simulation,precision_dt,scale

# care=rectangle(0.02,100000,0.2,1,[1,0.05],1,[0.2,1],[[0,0,0,0]],[0,0],0)#longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/10000,600)#temps_de_la_simulation,precision_dt,scale


# care=rectangle(0.03,100,0.5,1,[1,0.2],1,[0.2,0.8],[[0,0,0,0]],[0,0],0) #longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/3000,600)#temps_de_la_simulation,precision_dt,scale
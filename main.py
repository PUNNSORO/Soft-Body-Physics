import numpy as np
import time
from tkinter import *
import copy

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
        epsilon = 1*0.25/100

        # creation de la liste des deformations
        LIST_deformation = []
        for i in range(0, 46):
            LIST_deformation.append(epsilon)

        # creation de la liste des contrainte
        contrainte = [0, 14.5, 29, 37, 38, 38.5, 39, 39.5, 39.75, 40, 40.4, 40.6, 40.8, 41, 41.2, 41.4, 41.6, 41.8,
                      41.98, 42.16, 42.34, 42.42, 42.6, 42.75, 42.88
            , 43, 43.1, 43.2, 43.3, 43.4, 43.45, 43.49, 43.53, 43.575, 43.6, 43.65, 43.7, 43.7, 43.7, 43.7, 43.7, 43.65,
                      43.4, 43, 42.5, 42]

        for i in range(0,len(contrainte)):
            contrainte[i] = contrainte[i] * 10**7

        # determination du module de young initial
        young_init = contrainte[1]/LIST_deformation[1]
        coeff_poisson = 0.356

        # l'affectaion des ctes
        alpha = self.alpha
        l = self.len
        d = l*np.sqrt(2)
        dissip = self.dissip
        a = np.floor(self.dim[0]/l)*l
        b = np.floor(self.dim[1]/l)*l
        x = self.position[0]
        y = self.position[1]
        g = 9.81
        omega = self.rot

        # l'affectaion des raideurs
        kd = young_init * (3 * l) / (8 * (1 + coeff_poisson))
        k = young_init * l * (4 * coeff_poisson + 1) / (8 * (1 + coeff_poisson))

        # fonction qui clacule la distance entre 2 points
        def distance_entre(B, A):
            Ax = A[0]
            Ay = A[1]
            Bx = B[0]
            By = B[1]
            return np.sqrt((Bx - Ax) ** 2 + (By - Ay) ** 2)

        # fonction qui clacule la force appliquee par le ressort entre B et A sur A
        def force_ressort(B, A, l, k):
            Ax = A[0]
            Ay = A[1]
            Bx = B[0]
            By = B[1]
            AB = distance_entre(B, A)
            return [k * (l - AB) * (Ax - Bx) / AB, k * (l - AB) * (Ay - By) / AB]

        # l'initiation des matrices de position, vitese, acceleration, forces, et laison, aussi calcule du nombre de points
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
                nombre_de_points+=1
                L.append([x + l * j, y + l * i])
                K.append([0, 0])
                I.append([0, 0])
                T.append([0, 0])
                liaisons_2eme_coor_1er_pts = []
                for u in range(0, int(b / l)):
                    liaisons_1er_coor_2eme_pts = []
                    for z in range(0, int(a / l)):
                        liaisons_2eme_coor_2eme_pts = 0
                        liaisons_1er_coor_2eme_pts.append(liaisons_2eme_coor_2eme_pts)
                    liaisons_2eme_coor_1er_pts.append(liaisons_1er_coor_2eme_pts)
                liaisons_1er_coor_1er_pts.append(liaisons_2eme_coor_1er_pts)
            liaisons.append(liaisons_1er_coor_1er_pts)
            M.append(L)
            V.append(K)
            ACC.append(I)
            F.append(T)

        alpha = alpha/nombre_de_points

        # creation de la matrice liaison qui enregitre la longueur des ressorts, leurs raideurs, leurs courbe
        # contraite-def, leurs logueurs initiales et la distance entre les points a t-dt
        for i in range(0, len(M)):
            for j in range(0, len(M[0])):
                if i == 0:

                    if j == 0:
                        liaisons[i][j][i][j + 1] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i + 1][j + 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i + 1][j] = [l,k,[contrainte,LIST_deformation],l,l]

                    if j != 0 and j != len(M[0]) - 1:
                        liaisons[i][j][i][j + 1] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i + 1][j + 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i + 1][j] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i + 1][j - 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i][j - 1] = [l,k,[contrainte,LIST_deformation],l,l]

                    if j == len(M[0]) - 1:
                        liaisons[i][j][i + 1][j] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i + 1][j - 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i][j - 1] = [l,k,[contrainte,LIST_deformation],l,l]

                if i != 0 and i != len(M) - 1:

                    if j == 0:
                        liaisons[i][j][i][j + 1] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i + 1][j + 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i + 1][j] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i - 1][j] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i - 1][j + 1] = [d,kd,[contrainte,LIST_deformation],d,d]

                    if j != 0 and j != len(M[0]) - 1:
                        liaisons[i][j][i][j + 1] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i + 1][j + 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i + 1][j] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i + 1][j - 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i][j - 1] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i - 1][j - 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i - 1][j] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i - 1][j + 1] = [d,kd,[contrainte,LIST_deformation],d,d]

                    if j == len(M[0]) - 1:
                        liaisons[i][j][i + 1][j] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i + 1][j - 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i][j - 1] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i - 1][j - 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i - 1][j] = [l,k,[contrainte,LIST_deformation],l,l]

                if i == len(M) - 1:

                    if j == 0:
                        liaisons[i][j][i][j + 1] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i - 1][j] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i - 1][j + 1] = [d,kd,[contrainte,LIST_deformation],d,d]

                    if j != 0 and j != len(M[0]) - 1:
                        liaisons[i][j][i][j + 1] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i][j - 1] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i - 1][j - 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i - 1][j] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i - 1][j + 1] = [d,kd,[contrainte,LIST_deformation],d,d]

                    if j == len(M[0]) - 1:
                        liaisons[i][j][i][j - 1] = [l,k,[contrainte,LIST_deformation],l,l]
                        liaisons[i][j][i - 1][j - 1] = [d,kd,[contrainte,LIST_deformation],d,d]
                        liaisons[i][j][i - 1][j] = [l,k,[contrainte,LIST_deformation],l,l]


        epaisseur = 2

        #determination de la forme de la piece etudiee
        #CETTE PARTIE POUR LES CARRES
        if 1 == 1:
            for i in range(0, len(M)):
                for j in range(0, len(M[0])):
                    if i > epaisseur and i < len(M) - 1 - epaisseur and j > epaisseur and j < len(M) - 1 - epaisseur :
                        liaisons[i][j][i][j + 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                        liaisons[i][j + 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                        liaisons[i][j][i + 1][j + 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                        liaisons[i + 1][j + 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                        liaisons[i][j][i + 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                        liaisons[i + 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                        liaisons[i][j][i + 1][j - 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                        liaisons[i + 1][j - 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                        liaisons[i][j][i][j - 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                        liaisons[i][j - 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                        liaisons[i][j][i - 1][j - 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                        liaisons[i - 1][j - 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                        liaisons[i][j][i - 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                        liaisons[i - 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                        liaisons[i][j][i - 1][j + 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                        liaisons[i - 1][j + 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]

        # CETTE PARTIE POUR LES CERCLES
        if 1==0:
            for i in range(0, len(M)):
                for j in range(0, len(M[0])):
                    if (i-(1/(l*10))/2)**2 + (j-(1/(l*10))/2)**2 < 0**2 or (i-(1/(l*10))/2)**2 + (j-(1/(l*10))/2)**2 > 25**2 :
                        if i == 0:

                            if j == 0:
                                liaisons[i][j][i][j + 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j + 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i + 1][j + 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i + 1][j + 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i + 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i + 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]

                            if j != 0 and j != len(M[0]) - 1:
                                liaisons[i][j][i][j + 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j + 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i + 1][j + 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i + 1][j + 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i + 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i + 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i + 1][j - 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i + 1][j - 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i][j - 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j - 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]

                            if j == len(M[0]) - 1:
                                liaisons[i][j][i + 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i + 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i + 1][j - 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i + 1][j - 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i][j - 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j - 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]

                        if i != 0 and i != len(M) - 1:

                            if j == 0:
                                liaisons[i][j][i][j + 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j + 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i + 1][j + 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i + 1][j + 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i + 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i + 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i - 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i - 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i - 1][j + 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i - 1][j + 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]

                            if j != 0 and j != len(M[0]) - 1:
                                liaisons[i][j][i][j + 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j + 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i + 1][j + 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i + 1][j + 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i + 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i + 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i + 1][j - 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i + 1][j - 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i][j - 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j - 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i - 1][j - 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i - 1][j - 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i - 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i - 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i - 1][j + 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i - 1][j + 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]

                            if j == len(M[0]) - 1:
                                liaisons[i][j][i + 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i + 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i + 1][j - 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i + 1][j - 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i][j - 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j - 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i - 1][j - 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i - 1][j - 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i - 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i - 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]

                        if i == len(M) - 1:

                            if j == 0:
                                liaisons[i][j][i][j + 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j + 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i - 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i - 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i - 1][j + 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i - 1][j + 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]

                            if j != 0 and j != len(M[0]) - 1:
                                liaisons[i][j][i][j + 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j + 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i][j - 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j - 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i - 1][j - 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i - 1][j - 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i - 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i - 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i - 1][j + 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i - 1][j + 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]

                            if j == len(M[0]) - 1:
                                liaisons[i][j][i][j - 1] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j - 1][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i][j][i - 1][j - 1] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i - 1][j - 1][i][j] = [d, 0, [contrainte, LIST_deformation], d, d]
                                liaisons[i][j][i - 1][j] = [l, 0, [contrainte, LIST_deformation], l, l]
                                liaisons[i - 1][j][i][j] = [l, 0, [contrainte, LIST_deformation], l, l]


        # fonction qui calcule la deformation
        def deformation_calculation(Bi, Bj, Ai, Aj):
            epsilon = (distance_entre(M[Ai][Aj], M[Bi][Bj])-liaisons[Ai][Aj][Bi][Bj][0])/liaisons[Ai][Aj][Bi][Bj][0]

            return epsilon

        # fonction qui determine le module de young variable
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

        # fonction pour la reference
        def raideur(Bi, Bj, Ai, Aj):
            return young(Bi, Bj, Ai, Aj)

        # fonction qui change la raideur des ressort en fonction de plusieurs condition
        def update_raideur(Bi, Bj, Ai, Aj):

            deformation_t = deformation_calculation(Bi, Bj, Ai, Aj)
            new_distance = distance_entre(M[Ai][Aj], M[Bi][Bj])
            old_distance = liaisons[Ai][Aj][Bi][Bj][4]
            Deformation = liaisons[Ai][Aj][Bi][Bj][2][1]
            Contrainte = liaisons[Ai][Aj][Bi][Bj][2][0]
            distance_initial = liaisons[Ai][Aj][Bi][Bj][3]

            N = len(Contrainte)
            indice_de_deformation = int(1 + np.abs(np.floor((deformation_t - Deformation[1]) / LIST_deformation[1])))
            if distance_initial == l:
                new_raideur = raideur(Bi, Bj, Ai, Aj) * l * (4 * coeff_poisson + 1) / (8 * (1 + coeff_poisson))

            if distance_initial == d:
                new_raideur = raideur(Bi, Bj, Ai, Aj) * (3 * l) / (8 * (1 + coeff_poisson))

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
                    [liaisons[Ai][Aj][Bi][Bj][0], 0, [liaisons[Ai][Aj][Bi][Bj][2][0], liaisons[Ai][Aj][Bi][Bj][2][1]], liaisons[Ai][Aj][Bi][Bj][3], new_distance]

            if new_distance >= old_distance:
                if deformation_t > Deformation[len(Deformation)-1] :
                    return [liaisons[Ai][Aj][Bi][Bj][0], 0, [liaisons[Ai][Aj][Bi][Bj][2][0], liaisons[Ai][Aj][Bi][Bj][2][1]], liaisons[Ai][Aj][Bi][Bj][3], new_distance]
                else:
                    return [liaisons[Ai][Aj][Bi][Bj][0], new_raideur, [liaisons[Ai][Aj][Bi][Bj][2][0], liaisons[Ai][Aj][Bi][Bj][2][1]], liaisons[Ai][Aj][Bi][Bj][3], new_distance]


            else:
                if new_distance > old_distance:
                    return [new_distance, liaisons[Ai][Aj][Bi][Bj][1], [liaisons[Ai][Aj][Bi][Bj][2][0], liaisons[Ai][Aj][Bi][Bj][2][1]], liaisons[Ai][Aj][Bi][Bj][3], new_distance]
                else:
                    return [liaisons[Ai][Aj][Bi][Bj][0], liaisons[Ai][Aj][Bi][Bj][1], [liaisons[Ai][Aj][Bi][Bj][2][0], liaisons[Ai][Aj][Bi][Bj][2][1]], liaisons[Ai][Aj][Bi][Bj][3], new_distance]

        # repartir la mass sur les points
        m = self.mass/nombre_de_points

        # changer l'intensite du poids
        poids = -m*g*0

        #maintenant on reorganise quelque points suivant les commande de positions_de_qlq_points
        for o in self.start:
            i=o[0]
            j=o[1]
            M[i][j]=[M[i][j][0]+o[2]*l, M[i][j][1]+o[3]*l]

        # creation de la fenetre de visualisation
        W = 800
        H = 820
        window = Tk()
        canvas = Canvas(window, width=W, height=H, bg="white")
        canvas.pack()

        # fonction qui dessine les points
        def dessine_point(A):
            size=4
            canvas.create_oval(A[0]*s-size,H-A[1]*s+size,A[0]*s+size,H-A[1]*s-size,fill="black")

        # fonction qui dessine les points de la piece
        def dessine_les_points_de_la_matrice(M):
            for i in range(0, len(M)):
                for j in range(0, len(M[0])):
                    if (i-(1/(l*10))/2)**2 + (j-(1/(l*10))/2)**2 >= 0**2 and (i-(1/(l*10))/2)**2 + (j-(1/(l*10))/2)**2 <= 25**2 :
                        dessine_point(M[i][j])

        # fonction qui dessine une ligne entre deux points
        def dessine_ligne_entre(A,B):
            canvas.create_line(A[0]*s,H-A[1]*s,B[0]*s,H-B[1]*s,fill="red")

        # fonction qui aide a l'ecriture du code
        def A(L,i,j):
            return L[i][j]

        # fonction qui pivote un point
        def pivoter_point(A,B,phi):
            return [np.cos(phi)*(A[0]-B[0])-np.sin(phi)*(A[1]-B[1])+B[0],np.cos(phi)*(A[1]-B[1])+np.sin(phi)*(A[0]-B[0])+B[1]]

        # fonction qui pivote les points de la piece
        def pivoter_rectangle(M,B,phi):
            for i in range(0,len(M)):
                for j in range(0,len(M[0])):
                    M[i][j]=pivoter_point(M[i][j],B,phi)

        # fonction qui dessine les ressorts de la piece
        def dessine_lignes(M):
            for i in range(0,len(M)):
                for j in range(0,len(M[0])):
                    if i!=len(M)-1:

                        if j==0:
                            if liaisons[i][j][i+1][j][1] != 0:
                                dessine_ligne_entre(A(M, i, j), A(M, i + 1, j))
                            if liaisons[i][j][i][j+1][1] != 0:
                                dessine_ligne_entre(A(M, i, j), A(M, i, j + 1))
                            if liaisons[i][j][i+1][j+1][1] != 0:
                                dessine_ligne_entre(A(M, i, j), A(M, i + 1, j + 1))

                        if j!=0 and j!=len(M[0])-1:
                            if liaisons[i][j][i+1][j][1] != 0:
                                dessine_ligne_entre(A(M, i, j), A(M, i + 1, j))
                            if liaisons[i][j][i][j+1][1] != 0:
                                dessine_ligne_entre(A(M, i, j), A(M, i, j + 1))
                            if liaisons[i][j][i+1][j+1][1] != 0:
                                dessine_ligne_entre(A(M, i, j), A(M, i + 1, j + 1))
                            if liaisons[i][j][i+1][j-1][1] != 0:
                                dessine_ligne_entre(A(M, i, j), A(M, i + 1, j - 1))

                        if j==len(M[0])-1:
                            if liaisons[i][j][i+1][j][1] != 0:
                                dessine_ligne_entre(A(M, i, j), A(M, i + 1, j))
                            if liaisons[i][j][i+1][j-1][1] != 0:
                                dessine_ligne_entre(A(M, i, j), A(M, i + 1, j - 1))

                    if i==len(M)-1:
                        if j!=len(M[0])-1:
                            if liaisons[i][j][i][j+1][1] != 0:
                                dessine_ligne_entre(A(M, i, j), A(M, i, j + 1))

        # fonction qui met a jour les liaisons
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


        pivoter_rectangle(M,M[0][0],omega)
        dessine_lignes(M)
        # dessine_les_points_de_la_matrice(M)

        fixer_1er_ligne_y = 0  # 0 pour non 1 pour oui
        fixer_dernier_ligne_y = 0  # 0 pour non 1 pour oui
        fixer_1er_ligne_x = 0  # 0 pour non 1 pour oui
        duree_de_force = 1000

        number_of_frames=0

        # fonction qui calcule les forces et met a jour la matrice des forces
        def calculer_forces(M):
            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0]) - fixer_dernier_ligne_y):
                    if i <= epaisseur or i >= len(M) - 1 - epaisseur or j <= epaisseur or j >= len(M) - 1 - epaisseur :
                        if i == 0:

                            if j == 0:
                                F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0], liaisons[i][j][i][j + 1][1])
                                F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1][0], liaisons[i][j][i + 1][j + 1][1])
                                F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0], liaisons[i][j][i + 1][j][1])
                                Fr = [F1[0] + F2[0] + F3[0], F1[1] + F2[1] + F3[1]]

                            if j != 0 and j != len(M[0]) - 1:
                                F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0], liaisons[i][j][i][j + 1][1])
                                F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1][0], liaisons[i][j][i + 1][j + 1][1])
                                F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0], liaisons[i][j][i + 1][j][1])
                                F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1][0], liaisons[i][j][i + 1][j - 1][1])
                                F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0], liaisons[i][j][i][j - 1][1])
                                Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0], F1[1] + F2[1] + F3[1] + F4[1] + F5[1]]

                            if j == len(M[0]) - 1:
                                F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0], liaisons[i][j][i + 1][j][1])
                                F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1][0], liaisons[i][j][i + 1][j - 1][1])
                                F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0], liaisons[i][j][i][j - 1][1])
                                Fr = [F3[0] + F4[0] + F5[0], F3[1] + F4[1] + F5[1]]

                        if i != 0 and i != len(M) - 1:

                            if j == 0:
                                F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0], liaisons[i][j][i][j + 1][1])
                                F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1][0], liaisons[i][j][i + 1][j + 1][1])
                                F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0], liaisons[i][j][i + 1][j][1])
                                F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0], liaisons[i][j][i - 1][j][1])
                                F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1][0], liaisons[i][j][i - 1][j + 1][1])
                                Fr = [F1[0] + F2[0] + F3[0] + F7[0] + F8[0], F1[1] + F2[1] + F3[1] + F7[1] + F8[1]]

                            if j != 0 and j != len(M[0]) - 1:
                                F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0], liaisons[i][j][i][j + 1][1])
                                F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1][0], liaisons[i][j][i + 1][j + 1][1])
                                F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0], liaisons[i][j][i + 1][j][1])
                                F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1][0], liaisons[i][j][i + 1][j - 1][1])
                                F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0], liaisons[i][j][i][j - 1][1])
                                F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1][0], liaisons[i][j][i - 1][j - 1][1])
                                F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0], liaisons[i][j][i - 1][j][1])
                                F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1][0], liaisons[i][j][i - 1][j + 1][1])
                                Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0] + F6[0] + F7[0] + F8[0],
                                      F1[1] + F2[1] + F3[1] + F4[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                            if j == len(M[0]) - 1:
                                F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0], liaisons[i][j][i + 1][j][1])
                                F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1][0], liaisons[i][j][i + 1][j - 1][1])
                                F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0], liaisons[i][j][i][j - 1][1])
                                F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1][0], liaisons[i][j][i - 1][j - 1][1])
                                F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0], liaisons[i][j][i - 1][j][1])
                                Fr = [F3[0] + F4[0] + F5[0] + F6[0] + F7[0], F3[1] + F4[1] + F5[1] + F6[1] + F7[1]]

                        if i == len(M) - 1:

                            if j == 0:
                                F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0], liaisons[i][j][i][j + 1][1])
                                F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0], liaisons[i][j][i - 1][j][1])
                                F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1][0], liaisons[i][j][i - 1][j + 1][1])
                                Fr = [F1[0] + F7[0] + F8[0], F1[1] + F7[1] + F8[1]]

                            if j != 0 and j != len(M[0]) - 1:
                                F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0], liaisons[i][j][i][j + 1][1])
                                F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0], liaisons[i][j][i][j - 1][1])
                                F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1][0], liaisons[i][j][i - 1][j - 1][1])
                                F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0], liaisons[i][j][i - 1][j][1])
                                F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1][0], liaisons[i][j][i - 1][j + 1][1])
                                Fr = [F1[0] + F5[0] + F6[0] + F7[0] + F8[0], F1[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                            if j == len(M[0]) - 1:
                                F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0], liaisons[i][j][i][j - 1][1])
                                F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1][0], liaisons[i][j][i - 1][j - 1][1])
                                F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0], liaisons[i][j][i - 1][j][1])
                                Fr = [F5[0] + F6[0] + F7[0], F5[1] + F6[1] + F7[1]]

                        F[i][j] = Fr

        # fonction qui calcule les positions et met a jour la matrice des coordonnees
        def calculer_position(M,q):
            nombre_soumis = np.floor(q / 20)
            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0]) - fixer_dernier_ligne_y):
                    if i <= epaisseur or i >= len(M) - 1 - epaisseur or j <= epaisseur or j >= len(M) - 1 - epaisseur :
                        if i == 0 and j >= len(M[0]) - 1 - nombre_soumis and q < duree_de_force:
                            force_horizontale = -10 * 15 / (1 + nombre_soumis)
                            force_verticale = 0


                        else:
                            force_horizontale = 0
                            force_verticale = 0


                        ACC[i][j][0] = (F[i][j][0] - alpha * V[i][j][0] + force_horizontale) / m
                        ACC[i][j][1] = (F[i][j][1] - alpha * V[i][j][1] + poids + force_verticale) / m

                        M[i][j][0] = M[i][j][0] + V[i][j][0] * dt + dt ** 2 / 2 * ACC[i][j][0]
                        M[i][j][1] = M[i][j][1] + V[i][j][1] * dt + dt ** 2 / 2 * ACC[i][j][1]

        # fonction qui calcule les vitesses et met a jour la matrice des vitesses
        def calculer_vitesse(M):
            if np.floor(q/20)<=len(M):
                nombre_soumis = np.floor(q / 20)
            else:
                nombre_soumis = len(M)

            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0])-fixer_dernier_ligne_y):
                    if i <= epaisseur or i >= len(M) - 1 - epaisseur or j <= epaisseur or j >= len(M) - 1 - epaisseur :
                        if i == 0 and j >= len(M[0]) - 1 - nombre_soumis and q < duree_de_force:
                            force_horizontale = -10 * 15/(1+nombre_soumis)
                            force_verticale = 0

                        if i <= nombre_soumis and j >= len(M[0]) - 1 and q < duree_de_force:
                            force_horizontale = -10 * 15/(1+nombre_soumis)
                            force_verticale = 0

                        else:
                            force_horizontale = 0
                            force_verticale = 0

                        acc_Aij_x_1 = (F[i][j][0] - alpha * V[i][j][0] + force_horizontale) / m
                        acc_Aij_y_1 = (F[i][j][1] - alpha * V[i][j][1] + poids + force_verticale) / m

                        acc_Aij_x_0 = ACC[i][j][0]
                        acc_Aij_y_0 = ACC[i][j][1]

                        V[i][j][0] = V[i][j][0] + dt / 2 * (acc_Aij_x_1 + acc_Aij_x_0)
                        V[i][j][1] = V[i][j][1] + dt / 2 * (acc_Aij_y_1 + acc_Aij_y_0)


                        if M[i][j][0]<0: #les collisions avec le sol et les murs

                            M[i][j][0] = 0
                            V[i][j][0] = -V[i][j][0]*dissip

                        if M[i][j][1]<0:

                            M[i][j][1] = 0
                            V[i][j][1] = -V[i][j][1]*dissip


        # calcule d'energie
        aire = 0
        for i in range(1, len(contrainte)):
            aire += (contrainte[i] - contrainte[i-1]) * (LIST_deformation[i] - LIST_deformation[i-1])/2 + (LIST_deformation[i] - LIST_deformation[i-1]) * contrainte[i-1]

        def calculer_aire(List):
            aire_restante = 0
            list_deformation = List[2][1]
            list_contrainte = List[2][0]
            if List[1] == 0:
                if list_deformation == LIST_deformation:
                    return 0
                else:
                    return aire
            else:
                for i in range(1, len(list_contrainte)):
                    aire_restante += (list_contrainte[i] - list_contrainte[i - 1]) * (list_deformation[i] - list_deformation[i - 1]) / 2 + (
                                list_deformation[i] - list_deformation[i - 1]) * list_contrainte[i - 1]

            return aire - aire_restante

        def calculer_energie_indiv(List):
            return -calculer_aire(List) * List[3]

        def calcule_energie_absorbe(M):
            energie = 0
            for i in range(0, len(M)):
                for j in range(0, len(M[0])):
                    E = 0

                    if i != 0 and i != len(M) - 1:

                        if j == 0:
                            E = calculer_energie_indiv(liaisons[i][j][i][j + 1])
                            E += calculer_energie_indiv(liaisons[i][j][i + 1][j + 1])
                            E += calculer_energie_indiv(liaisons[i][j][i + 1][j])

                        if j != 0 and j != len(M[0]) - 1:
                            E = calculer_energie_indiv(liaisons[i][j][i][j + 1])
                            E += calculer_energie_indiv(liaisons[i][j][i + 1][j + 1])
                            E += calculer_energie_indiv(liaisons[i][j][i + 1][j])
                            E += calculer_energie_indiv(liaisons[i][j][i + 1][j - 1])

                        if j == len(M[0]) - 1:
                            E = calculer_energie_indiv(liaisons[i][j][i + 1][j])
                            E += calculer_energie_indiv(liaisons[i][j][i + 1][j - 1])

                    if i == len(M) - 1:

                        if j != len(M[0]) - 1:
                            E = calculer_energie_indiv(liaisons[i][j][i][j + 1])

                    energie += E

            return energie

        # commencement de la boucle de temps
        for q in range(0,int(t/dt)):
            start_time=time.time()

            calculer_forces(M)

            calculer_position(M, q)

            update_les_ressort(M)

            calculer_forces(M)

            calculer_vitesse(M)

            if q == duree_de_force :
                print("energie total: ### ",calcule_energie_absorbe(M)," x S  ###")

            #methode d'Euler
            # for i in range(fixer_1er_ligne_x, len(M)):
            #     for j in range(fixer_1er_ligne_y, len(M[0])):
            #         if i == len(M)-1 and j == len(M[0])-1 and q<duree_de_force:
            #             force_horizontale = 1
            #             force_verticale = 1
            #
            #         else:
            #             force_horizontale = 0
            #             force_verticale = 0
            #
            #         ACC[i][j][0] = (F[i][j][0] - alpha * V[i][j][0] + force_horizontale) / m
            #         ACC[i][j][1] = (F[i][j][1] - alpha * V[i][j][1] + poids + force_verticale) / m
            #
            #
            #         V[i][j][0] += ACC[i][j][0] * dt
            #         V[i][j][1] += ACC[i][j][1] * dt
            #
            #         M[i][j][0] += V[i][j][0] * dt
            #         M[i][j][1] += V[i][j][1] * dt


                    #methode d'Euler:

                    # V[i][j][0] = V[i][j][0] + ACC[i][j][0] * dt
                    # V[i][j][1] = V[i][j][1] + ACC[i][j][1] * dt
                    #
                    # M[i][j][0] = M[i][j][0] + V[i][j][0] * dt
                    # M[i][j][1] = M[i][j][1] + V[i][j][1] * dt
                    #
                    # if M[i][j][0]<0: #les collisions avec le sol et les murs
                    #
                    #     M[i][j][0] = 0
                    #     V[i][j][0] = -V[i][j][0]*dissip
                    #
                    # if M[i][j][1]<0:
                    #
                    #     M[i][j][1] = 0
                    #     V[i][j][1] = -V[i][j][1]*dissip

            end_time=time.time()

            frame_calculation_time=end_time-start_time

            canvas.delete("all")
            dessine_lignes(M)
            #dessine_les_points_de_la_matrice(M)


            number_of_frames+=1
            print(number_of_frames*dt,"-------",q)


            window.update()

        window.mainloop()

# ------------ LES SIMULATIONS -------------

# care=rectangle(1/10,1000,0.5,1,[1,0.2],1,[0.2,1],[[0,0,0,0]],[0,0],np.pi/6) #longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/300,300)#temps_de_la_simulation,precision_dt,scale

care=rectangle(1/500,50,0.5,20,[0.1,0.1],1,[0.07,0.01],[[0,0,0,0]],[0,0],np.pi /4)#longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
care.simuler(100000,1/(600*150),5000)#temps_de_la_simulation,precision_dt,scale,forme

# care=rectangle(1/20,25,0.5,0.2,[0.1,0.1],1,[0.1,0.1],[[0,0,0,0]],[0,0],0)#longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/5000,2000)#temps_de_la_simulation,precision_dt,scale

# care=rectangle(0.02,100000,0.2,1,[1,0.05],1,[0.2,1],[[0,0,0,0]],[0,0],0)#longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/10000,600)#temps_de_la_simulation,precision_dt,scale


# care=rectangle(0.03,100,0.5,1,[1,0.2],1,[0.2,0.8],[[0,0,0,0]],[0,0],0) #longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/3000,600)#temps_de_la_simulation,precision_dt,scale
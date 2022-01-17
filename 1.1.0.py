import numpy as np
import time
from tkinter import *
import copy
import keyboard

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

        LIST_deformation = []
        for i in range(0, 46):
            LIST_deformation.append(i * 0.25/100)

        contrainte = [0, 14.5, 29, 37, 38, 38.5, 39, 39.5, 39.75, 40, 40.4, 40.6, 40.8, 41, 41.2, 41.4, 41.6, 41.8,
                      41.98, 42.16, 42.34, 42.42, 42.6, 42.75, 42.88
            , 43, 43.1, 43.2, 43.3, 43.4, 43.45, 43.49, 43.53, 43.575, 43.6, 43.65, 43.7, 43.7, 43.7, 43.7, 43.7, 43.65,
                      43.4, 43, 42.5, 42]

        for i in range(0,len(contrainte)):
            contrainte[i] = contrainte[i]*6

        young_init = contrainte[1]/LIST_deformation[1]
        k = young_init

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

        #M est la matrice representant les points du solide

        def distance_entre(B, A):
            Ax = A[0]
            Ay = A[1]
            Bx = B[0]
            By = B[1]
            return np.sqrt((Bx - Ax) ** 2 + (By - Ay) ** 2)


        def force_ressort(B, A, l, k):  # force appliquée par le ressort se situant entre B et A sur A
            Ax = A[0]
            Ay = A[1]
            Bx = B[0]
            By = B[1]
            AB = distance_entre(B, A)
            return [k * (l - AB) * (Ax - Bx) / AB, k * (l - AB) * (Ay - By) / AB]

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

        for i in range(0, len(M)):
            for j in range(0, len(M[0])):
                if i == 0:

                    if j == 0:
                        liaisons[i][j][i][j + 1] = [l,k]
                        liaisons[i][j][i + 1][j + 1] = [d,k]
                        liaisons[i][j][i + 1][j] = [l,k]

                    if j != 0 and j != len(M[0]) - 1:
                        liaisons[i][j][i][j + 1] = [l,k]
                        liaisons[i][j][i + 1][j + 1] = [d,k]
                        liaisons[i][j][i + 1][j] = [l,k]
                        liaisons[i][j][i + 1][j - 1] = [d,k]
                        liaisons[i][j][i][j - 1] = [l,k]

                    if j == len(M[0]) - 1:
                        liaisons[i][j][i + 1][j] = [l,k]
                        liaisons[i][j][i + 1][j - 1] = [d,k]
                        liaisons[i][j][i][j - 1] = [l,k]

                if i != 0 and i != len(M) - 1:

                    if j == 0:
                        liaisons[i][j][i][j + 1] = [l,k]
                        liaisons[i][j][i + 1][j + 1] = [d,k]
                        liaisons[i][j][i + 1][j] = [l,k]
                        liaisons[i][j][i - 1][j] = [l,k]
                        liaisons[i][j][i - 1][j + 1] = [d,k]

                    if j != 0 and j != len(M[0]) - 1:
                        liaisons[i][j][i][j + 1] = [l,k]
                        liaisons[i][j][i + 1][j + 1] = [d,k]
                        liaisons[i][j][i + 1][j] = [l,k]
                        liaisons[i][j][i + 1][j - 1] = [d,k]
                        liaisons[i][j][i][j - 1] = [l,k]
                        liaisons[i][j][i - 1][j - 1] = [d,k]
                        liaisons[i][j][i - 1][j] = [l,k]
                        liaisons[i][j][i - 1][j + 1] = [d,k]

                    if j == len(M[0]) - 1:
                        liaisons[i][j][i + 1][j] = [l,k]
                        liaisons[i][j][i + 1][j - 1] = [d,k]
                        liaisons[i][j][i][j - 1] = [l,k]
                        liaisons[i][j][i - 1][j - 1] = [d,k]
                        liaisons[i][j][i - 1][j] = [l,k]

                if i == len(M) - 1:

                    if j == 0:
                        liaisons[i][j][i][j + 1] = [l,k]
                        liaisons[i][j][i - 1][j] = [l,k]
                        liaisons[i][j][i - 1][j + 1] = [d,k]

                    if j != 0 and j != len(M[0]) - 1:
                        liaisons[i][j][i][j + 1] = [l,k]
                        liaisons[i][j][i][j - 1] = [l,k]
                        liaisons[i][j][i - 1][j - 1] = [d,k]
                        liaisons[i][j][i - 1][j] = [l,k]
                        liaisons[i][j][i - 1][j + 1] = [d,k]

                    if j == len(M[0]) - 1:
                        liaisons[i][j][i][j - 1] = [l,k]
                        liaisons[i][j][i - 1][j - 1] = [d,k]
                        liaisons[i][j][i - 1][j] = [l,k]


        liaisons_initiales = copy.deepcopy(liaisons)

        def deformation (Bi, Bj, Ai, Aj):
            epsilon = (distance_entre(M[Ai][Aj], M[Bi][Bj])-liaisons[Ai][Aj][Bi][Bj][0])/liaisons[Ai][Aj][Bi][Bj][0]

            return epsilon

        def young(Bi, Bj, Ai, Aj):
            if liaisons[Ai][Aj][Bi][Bj][1] != 0:
                if deformation(Bi, Bj, Ai, Aj) > 0 :
                    if deformation(Bi, Bj, Ai, Aj) >= LIST_deformation[len(LIST_deformation)-1]:
                        return 0
                    else:
                        indice = int(np.floor(deformation(Bi, Bj, Ai, Aj))/LIST_deformation[1])
                        return (contrainte[indice+1]-contrainte[indice])/LIST_deformation[1]

                if deformation(Bi, Bj, Ai, Aj) <= 0:
                    return k

            if liaisons[Ai][Aj][Bi][Bj][1] == 0:
                return 0

        m = self.mass/nombre_de_points

        poids = -m*g

        #maintenant on reorganise quelque points suivant les commande de positions_de_qlq_points

        for o in self.start:
            i=o[0]
            j=o[1]
            M[i][j]=[M[i][j][0]+o[2]*l, M[i][j][1]+o[3]*l]

        W = 800
        H = 650
        window = Tk()
        canvas = Canvas(window, width=W, height=H, bg="white")
        canvas.pack()

        def dessine_point(A):
            size=4
            canvas.create_oval(A[0]*s-size,H-A[1]*s+size,A[0]*s+size,H-A[1]*s-size,fill="black")

        def dessine_les_points_de_la_matrice(M):
            for i in M:
                for p in i:
                    dessine_point(p)

        def dessine_ligne_entre(A,B):
            canvas.create_line(A[0]*s,H-A[1]*s,B[0]*s,H-B[1]*s,fill="red")

        def A(L,i,j): #une fonction qui aidera á bien organiser les points de la matrice
            return L[i][j]

        def pivoter_point(A,B,phi):
            return [np.cos(phi)*(A[0]-B[0])-np.sin(phi)*(A[1]-B[1])+B[0],np.cos(phi)*(A[1]-B[1])+np.sin(phi)*(A[0]-B[0])+B[1]]

        def pivoter_rectangle(M,B,phi):
            for i in range(0,len(M)):
                for j in range(0,len(M[0])):
                    M[i][j]=pivoter_point(M[i][j],B,phi)

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

        pivoter_rectangle(M,M[0][0],omega)
        dessine_lignes(M)
        dessine_les_points_de_la_matrice(M)

        fixer_1er_ligne_y = 0  # 0 pour non 1 pour oui
        fixer_dernier_ligne_y = 0  # 0 pour non 1 pour oui
        fixer_1er_ligne_x = 0  # 0 pour non 1 pour oui
        duree_de_force = 0

        number_of_frames=0

        for q in range(0,int(t/dt)):
            start_time=time.time()
            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0])-fixer_dernier_ligne_y):
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




            # for i in range(fixer_1er_ligne_x, len(M)):
            #     for j in range(fixer_1er_ligne_y, len(M[0])):
            #         if i == 0:
            #
            #             if j == 0:
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j + 1] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j + 1] = distance_entre(M[i + 1][j + 1], M[i][j])
            #                 if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j + 1] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j] = 'coupe'
            #
            #             if j != 0 and j != len(M[0]) - 1:
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j + 1] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j + 1] = distance_entre(M[i + 1][j + 1], M[i][j])
            #                 if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j + 1] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j - 1] = distance_entre(M[i + 1][j - 1], M[i][j])
            #                 if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j - 1] = 'coupe'
            #
            #             if j == len(M[0]) - 1:
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j - 1] = distance_entre(M[i + 1][j - 1], M[i][j])
            #                 if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j - 1] = 'coupe'
            #
            #         if i != 0 and i != len(M) - 1:
            #
            #             if j == 0:
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j + 1] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j + 1] = distance_entre(M[i + 1][j + 1], M[i][j])
            #                 if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j + 1] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j + 1] = distance_entre(M[i - 1][j + 1], M[i][j])
            #                 if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j + 1] = 'coupe'
            #
            #             if j != 0 and j != len(M[0]) - 1:
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j + 1] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j + 1] = distance_entre(M[i + 1][j + 1], M[i][j])
            #                 if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j + 1] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j - 1] = distance_entre(M[i + 1][j - 1], M[i][j])
            #                 if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j - 1] = distance_entre(M[i - 1][j - 1], M[i][j])
            #                 if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j + 1] = distance_entre(M[i - 1][j + 1], M[i][j])
            #                 if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j + 1] = 'coupe'
            #
            #             if j == len(M[0]) - 1:
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])
            #                 if np.absolute(deformation([i + 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j] = 'coupe'
            #                 if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i + 1][j - 1] = distance_entre(M[i + 1][j - 1], M[i][j])
            #                 if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i + 1][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j - 1] = distance_entre(M[i - 1][j - 1], M[i][j])
            #                 if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j] = 'coupe'
            #
            #         if i == len(M) - 1:
            #
            #             if j == 0:
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j + 1] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j + 1] = distance_entre(M[i - 1][j + 1], M[i][j])
            #                 if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j + 1] = 'coupe'
            #
            #             if j != 0 and j != len(M[0]) - 1:
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
            #                 if np.absolute(deformation([i,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j + 1] = 'coupe'
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j - 1] = distance_entre(M[i - 1][j - 1], M[i][j])
            #                 if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j + 1] = distance_entre(M[i - 1][j + 1], M[i][j])
            #                 if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j + 1] = 'coupe'
            #
            #             if j == len(M[0]) - 1:
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])
            #                 if np.absolute(deformation([i,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j - 1] = distance_entre(M[i - 1][j - 1], M[i][j])
            #                 if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j - 1] = 'coupe'
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
            #                     liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])
            #                 if np.absolute(deformation([i - 1,j], [i,j])) > limite_deplasticite:
            #                     liaisons[i][j][i - 1][j] = 'coupe'

            # this works perfectly

            # ACC[1][0][0] = (F[1][0][0] - alpha * V10x ) / m
            # ACC[1][0][1] = (F[1][0][1]  - alpha * V10y ) / m
            #
            # V10x += ACC[1][0][0] * dt
            # V10y += ACC[1][0][1] * dt
            #
            # M[1][0][0] += V10x * dt
            # M[1][0][1] += V10y * dt
            #
            # ACC[1][1][0] = (F[1][1][0] - alpha * V11x) / m
            # ACC[1][1][1] = (F[1][1][1] - alpha * V11y ) / m
            #
            # V11x += ACC[1][1][0] * dt
            # V11y += ACC[1][1][1] * dt
            #
            # M[1][1][0] += V11x * dt
            # M[1][1][1] += V11y * dt

            #issue with the velociy matrix
            #
            # ACC[1][0][0] = (F[1][0][0] - alpha * V[1][0][0]) / m
            # ACC[1][0][1] = (F[1][0][1] - alpha * V[1][0][1]) / m
            #
            # V[1][0][0] += ACC[1][0][0] * dt
            # V[1][0][1] += ACC[1][0][1] * dt
            #
            # M[1][0][0] += V[1][0][0] * dt
            # M[1][0][1] += V[1][0][1] * dt
            #
            # ACC[1][1][0] = (F[1][1][0] - alpha * V[1][1][0]) / m
            # ACC[1][1][1] = (F[1][1][1] - alpha * V[1][1][1]) / m
            #
            # V[1][1][0] += ACC[1][1][0] * dt
            # V[1][1][1] += ACC[1][1][1] * dt
            #
            # M[1][1][0] += V[1][1][0] * dt
            # M[1][1][1] += V[1][1][1] * dt



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

            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0])-fixer_dernier_ligne_y):
                    if i == 1 and j == np.floor(len(M[0])/2-1) and q < duree_de_force:
                        force_horizontale = 0
                        force_verticale = -35


                    else:
                        force_horizontale = 0
                        force_verticale = 0

                    ACC[i][j][0] = (F[i][j][0] - alpha * V[i][j][0] + force_horizontale) / m
                    ACC[i][j][1] = (F[i][j][1] - alpha * V[i][j][1] + poids + force_verticale) / m

                    M[i][j][0] = M[i][j][0] + V[i][j][0] * dt + dt ** 2 / 2 * ACC[i][j][0]
                    M[i][j][1] = M[i][j][1] + V[i][j][1] * dt + dt ** 2 / 2 * ACC[i][j][1]

            for i in range(0, len(M)):
                for j in range(0, len(M[0])):
                    if i == 0:

                        if j == 0:
                            liaisons[i][j][i][j + 1][1] = young(i ,j + 1, i,j)
                            liaisons[i][j][i + 1][j + 1][1] = young(i + 1,j + 1, i,j)
                            liaisons[i][j][i + 1][j][1] = young(i + 1, j, i,j)

                        if j != 0 and j != len(M[0]) - 1:
                            liaisons[i][j][i][j + 1][1] = young(i ,j + 1, i,j)
                            liaisons[i][j][i + 1][j + 1][1] = young(i + 1,j + 1, i,j)
                            liaisons[i][j][i + 1][j][1] = young(i + 1, j, i,j)
                            liaisons[i][j][i + 1][j - 1][1] = young(i + 1,j - 1, i,j)
                            liaisons[i][j][i][j - 1][1] = young(i ,j - 1, i,j)

                        if j == len(M[0]) - 1:
                            liaisons[i][j][i + 1][j][1] = young(i + 1,j , i,j)
                            liaisons[i][j][i + 1][j - 1][1] = young(i + 1,j - 1, i,j)
                            liaisons[i][j][i][j - 1][1] = young(i ,j - 1, i,j)

                    if i != 0 and i != len(M) - 1:

                        if j == 0:
                            liaisons[i][j][i][j + 1][1] = young(i ,j + 1, i,j)
                            liaisons[i][j][i + 1][j + 1][1] = young(i + 1,j + 1, i,j)
                            liaisons[i][j][i + 1][j][1] = young(i + 1, j, i,j)
                            liaisons[i][j][i - 1][j][1] = young(i - 1, j, i,j)
                            liaisons[i][j][i - 1][j + 1][1] = young(i - 1,j + 1, i,j)

                        if j != 0 and j != len(M[0]) - 1:
                            liaisons[i][j][i][j + 1][1] = young(i ,j + 1, i,j)
                            liaisons[i][j][i + 1][j + 1][1] = young(i + 1,j + 1, i,j)
                            liaisons[i][j][i + 1][j][1] = young(i + 1, j, i,j)
                            liaisons[i][j][i + 1][j - 1][1] = young(i + 1,j - 1, i,j)
                            liaisons[i][j][i][j - 1][1] = young(i ,j - 1, i,j)
                            liaisons[i][j][i - 1][j - 1][1] = young(i - 1,j - 1, i,j)
                            liaisons[i][j][i - 1][j][1] = young(i - 1, j, i,j)
                            liaisons[i][j][i - 1][j + 1][1] = young(i - 1,j + 1, i,j)

                        if j == len(M[0]) - 1:
                            liaisons[i][j][i + 1][j][1] = young(i + 1,j, i,j)
                            liaisons[i][j][i + 1][j - 1][1] = young(i + 1,j - 1, i,j)
                            liaisons[i][j][i][j - 1][1] = young(i ,j - 1, i,j)
                            liaisons[i][j][i - 1][j - 1][1] = young(i - 1,j - 1, i,j)
                            liaisons[i][j][i - 1][j][1] = young(i - 1, j, i,j)

                    if i == len(M) - 1:

                        if j == 0:
                            liaisons[i][j][i][j + 1][1] = young(i ,j + 1, i,j)
                            liaisons[i][j][i - 1][j][1] = young(i - 1,j, i,j)
                            liaisons[i][j][i - 1][j + 1][1] = young(i - 1,j + 1, i,j)

                        if j != 0 and j != len(M[0]) - 1:
                            liaisons[i][j][i][j + 1][1] = young(i ,j + 1, i,j)
                            liaisons[i][j][i][j - 1][1] = young(i ,j - 1, i,j)
                            liaisons[i][j][i - 1][j - 1][1] = young(i - 1,j - 1, i,j)
                            liaisons[i][j][i - 1][j][1] = young(i - 1,j, i,j)
                            liaisons[i][j][i - 1][j + 1][1] = young(i - 1,j + 1, i,j)

                        if j == len(M[0]) - 1:
                            liaisons[i][j][i][j - 1][1] = young(i ,j - 1, i,j)
                            liaisons[i][j][i - 1][j - 1][1] = young(i - 1,j - 1, i,j)
                            liaisons[i][j][i - 1][j][1] = young(i - 1, j, i,j)


            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0]) - fixer_dernier_ligne_y):
                    if i == 0:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0],
                                               liaisons[i][j][i][j + 1][1])
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1][0],
                                               liaisons[i][j][i + 1][j + 1][1])
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0],
                                               liaisons[i][j][i + 1][j][1])
                            Fr = [F1[0] + F2[0] + F3[0], F1[1] + F2[1] + F3[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0],
                                               liaisons[i][j][i][j + 1][1])
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1][0],
                                               liaisons[i][j][i + 1][j + 1][1])
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0],
                                               liaisons[i][j][i + 1][j][1])
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1][0],
                                               liaisons[i][j][i + 1][j - 1][1])
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0],
                                               liaisons[i][j][i][j - 1][1])
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0], F1[1] + F2[1] + F3[1] + F4[1] + F5[1]]

                        if j == len(M[0]) - 1:
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0],
                                               liaisons[i][j][i + 1][j][1])
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1][0],
                                               liaisons[i][j][i + 1][j - 1][1])
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0],
                                               liaisons[i][j][i][j - 1][1])
                            Fr = [F3[0] + F4[0] + F5[0], F3[1] + F4[1] + F5[1]]

                    if i != 0 and i != len(M) - 1:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0],
                                               liaisons[i][j][i][j + 1][1])
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1][0],
                                               liaisons[i][j][i + 1][j + 1][1])
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0],
                                               liaisons[i][j][i + 1][j][1])
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0],
                                               liaisons[i][j][i - 1][j][1])
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1][0],
                                               liaisons[i][j][i - 1][j + 1][1])
                            Fr = [F1[0] + F2[0] + F3[0] + F7[0] + F8[0], F1[1] + F2[1] + F3[1] + F7[1] + F8[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0],
                                               liaisons[i][j][i][j + 1][1])
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1][0],
                                               liaisons[i][j][i + 1][j + 1][1])
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0],
                                               liaisons[i][j][i + 1][j][1])
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1][0],
                                               liaisons[i][j][i + 1][j - 1][1])
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0],
                                               liaisons[i][j][i][j - 1][1])
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1][0],
                                               liaisons[i][j][i - 1][j - 1][1])
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0],
                                               liaisons[i][j][i - 1][j][1])
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1][0],
                                               liaisons[i][j][i - 1][j + 1][1])
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0] + F6[0] + F7[0] + F8[0],
                                  F1[1] + F2[1] + F3[1] + F4[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j][0],
                                               liaisons[i][j][i + 1][j][1])
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1][0],
                                               liaisons[i][j][i + 1][j - 1][1])
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0],
                                               liaisons[i][j][i][j - 1][1])
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1][0],
                                               liaisons[i][j][i - 1][j - 1][1])
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0],
                                               liaisons[i][j][i - 1][j][1])
                            Fr = [F3[0] + F4[0] + F5[0] + F6[0] + F7[0], F3[1] + F4[1] + F5[1] + F6[1] + F7[1]]

                    if i == len(M) - 1:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0],
                                               liaisons[i][j][i][j + 1][1])
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0],
                                               liaisons[i][j][i - 1][j][1])
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1][0],
                                               liaisons[i][j][i - 1][j + 1][1])
                            Fr = [F1[0] + F7[0] + F8[0], F1[1] + F7[1] + F8[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1][0],
                                               liaisons[i][j][i][j + 1][1])
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0],
                                               liaisons[i][j][i][j - 1][1])
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1][0],
                                               liaisons[i][j][i - 1][j - 1][1])
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0],
                                               liaisons[i][j][i - 1][j][1])
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1][0],
                                               liaisons[i][j][i - 1][j + 1][1])
                            Fr = [F1[0] + F5[0] + F6[0] + F7[0] + F8[0], F1[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1][0],
                                               liaisons[i][j][i][j - 1][1])
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1][0],
                                               liaisons[i][j][i - 1][j - 1][1])

                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j][0],
                                               liaisons[i][j][i - 1][j][1])
                            Fr = [F5[0] + F6[0] + F7[0], F5[1] + F6[1] + F7[1]]

                    F[i][j] = Fr



            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0])-fixer_dernier_ligne_y):
                    if i == 1 and j == np.floor(len(M[0])/2 - 1) and q < duree_de_force:
                        force_horizontale = 0
                        force_verticale = -35

                    else:
                        force_horizontale = 0
                        force_verticale = 0

                    acc_Aij_x_1 = (F[i][j][0] - alpha * V[i][j][0] + force_horizontale) / m
                    acc_Aij_y_1 = (F[i][j][1] - alpha * V[i][j][1] + poids + force_verticale) / m

                    acc_Aij_x_0 = ACC[i][j][0]
                    acc_Aij_y_0 = ACC[i][j][1]

                    V[i][j][0] = V[i][j][0] + dt / 2 * (acc_Aij_x_1 + acc_Aij_x_0)
                    V[i][j][1] = V[i][j][1] + dt / 2 * (acc_Aij_y_1 + acc_Aij_y_0)

                    if keyboard.is_pressed('a'):
                        print('yes')
                        V[i][j][0] = V[i][j][0] - 0.1
                    if keyboard.is_pressed('d'):
                        V[i][j][0] = V[i][j][0] + 0.1
                    if keyboard.is_pressed('s'):
                        V[i][j][1] = V[i][j][1] - 0.1
                    if keyboard.is_pressed('w'):
                        V[i][j][1] = V[i][j][1] + 0.1

                    if M[i][j][0]<0: #les collisions avec le sol et les murs

                        M[i][j][0] = 0
                        V[i][j][0] = -V[i][j][0]*dissip

                    if M[i][j][1]<0:

                        M[i][j][1] = 0
                        V[i][j][1] = -V[i][j][1]*dissip

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

care=rectangle(1/10,100,0.5,20,[1,1],1,[0.7,1],[[0,0,0,0]],[0,0],np.pi/6)#longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
care.simuler(10000,1/1000,300)#temps_de_la_simulation,precision_dt,scale

# care=rectangle(1/20,25,0.5,0.2,[0.1,0.1],1,[0.1,0.1],[[0,0,0,0]],[0,0],0)#longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/5000,2000)#temps_de_la_simulation,precision_dt,scale

# care=rectangle(0.02,100000,0.2,1,[1,0.05],1,[0.2,1],[[0,0,0,0]],[0,0],0)#longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/10000,600)#temps_de_la_simulation,precision_dt,scale


# care=rectangle(0.03,100,0.5,1,[1,0.2],1,[0.2,0.8],[[0,0,0,0]],[0,0],0) #longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/3000,600)#temps_de_la_simulation,precision_dt,scale

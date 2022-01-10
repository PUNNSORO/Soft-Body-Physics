import numpy as np
import time
from tkinter import *

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

        alpha = self.alpha
        l = self.len
        d = l*np.sqrt(2)
        k = self.stif
        dissip = self.dissip
        a = np.floor(self.dim[0]/l)*l
        b = np.floor(self.dim[1]/l)*l
        x = self.position[0]
        y = self.position[1]
        g = 9.81
        omega = self.rot

        limite_delasticite = 1

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
                K.append(self.vit)
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
                        liaisons[i][j][i][j + 1] = l
                        liaisons[i][j][i + 1][j + 1] = d
                        liaisons[i][j][i + 1][j] = l

                    if j != 0 and j != len(M[0]) - 1:
                        liaisons[i][j][i][j + 1] = l
                        liaisons[i][j][i + 1][j + 1] = d
                        liaisons[i][j][i + 1][j] = l
                        liaisons[i][j][i + 1][j - 1] = d
                        liaisons[i][j][i][j - 1] = l

                    if j == len(M[0]) - 1:
                        liaisons[i][j][i + 1][j] = l
                        liaisons[i][j][i + 1][j - 1] = d
                        liaisons[i][j][i][j - 1] = l

                if i != 0 and i != len(M) - 1:

                    if j == 0:
                        liaisons[i][j][i][j + 1] = l
                        liaisons[i][j][i + 1][j + 1] = d
                        liaisons[i][j][i + 1][j] = l
                        liaisons[i][j][i - 1][j] = l
                        liaisons[i][j][i - 1][j + 1] = d

                    if j != 0 and j != len(M[0]) - 1:
                        liaisons[i][j][i][j + 1] = l
                        liaisons[i][j][i + 1][j + 1] = d
                        liaisons[i][j][i + 1][j] = l
                        liaisons[i][j][i + 1][j - 1] = d
                        liaisons[i][j][i][j - 1] = l
                        liaisons[i][j][i - 1][j - 1] = d
                        liaisons[i][j][i - 1][j] = l
                        liaisons[i][j][i - 1][j + 1] = d

                    if j == len(M[0]) - 1:
                        liaisons[i][j][i + 1][j] = l
                        liaisons[i][j][i + 1][j - 1] = d
                        liaisons[i][j][i][j - 1] = l
                        liaisons[i][j][i - 1][j - 1] = d
                        liaisons[i][j][i - 1][j] = l

                if i == len(M) - 1:

                    if j == 0:
                        liaisons[i][j][i][j + 1] = l
                        liaisons[i][j][i - 1][j] = l
                        liaisons[i][j][i - 1][j + 1] = d

                    if j != 0 and j != len(M[0]) - 1:
                        liaisons[i][j][i][j + 1] = l
                        liaisons[i][j][i][j - 1] = l
                        liaisons[i][j][i - 1][j - 1] = d
                        liaisons[i][j][i - 1][j] = l
                        liaisons[i][j][i - 1][j + 1] = d

                    if j == len(M[0]) - 1:
                        liaisons[i][j][i][j - 1] = l
                        liaisons[i][j][i - 1][j - 1] = d
                        liaisons[i][j][i - 1][j] = l

        liaisons_initiales = liaisons

        def deformation (B, A):
            Ai = A[0]
            Aj = A[1]
            Bi = B[0]
            Bj = B[1]
            epsilon = (distance_entre(M[Ai][Aj], M[Bi][Bj])-liaisons_initiales[Ai][Aj][Bi][Bj])/liaisons_initiales[Ai][Aj][Bi][Bj]

            return epsilon

        m = self.mass/nombre_de_points

        poids = - m * g

        #maintenant on reorganise quelque points suivant les commande de positions_de_qlq_points

        for o in self.start:
            i=o[0]
            j=o[1]
            M[i][j]=[x+(i+o[2])*l,y+(j+o[3])*l]

        W = 800
        H = 650
        window = Tk()
        canvas = Canvas(window, width=W, height=H, bg="white")
        canvas.pack()

        def dessine_point(A):
            canvas.create_rectangle(A[0]*s-1,H-A[1]*s+1,A[0]*s+2,H-A[1]*s-2,fill="black")

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

        pivoter_rectangle(M,M[0][0],omega)
        dessine_lignes(M)
        dessine_les_points_de_la_matrice(M)

        fixer_1er_ligne_y = 1  # 0 pour non 1 pour oui
        fixer_1er_ligne_x = 0  # 0 pour non 1 pour oui

        number_of_frames=0
        for q in range(0,int(t/dt)):
            start_time=time.time()
            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0])):
                    if i == 0:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1], k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            Fr = [F1[0] + F2[0] + F3[0], F1[1] + F2[1] + F3[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1], k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1], k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0], F1[1] + F2[1] + F3[1] + F4[1] + F5[1]]

                        if j == len(M[0]) - 1:
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1], k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            Fr = [F3[0] + F4[0] + F5[0], F3[1] + F4[1] + F5[1]]

                    if i != 0 and i != len(M) - 1:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1], k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1], k)
                            Fr = [F1[0] + F2[0] + F3[0] + F7[0] + F8[0], F1[1] + F2[1] + F3[1] + F7[1] + F8[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1], k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1], k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1], k)
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0] + F6[0] + F7[0] + F8[0],
                                  F1[1] + F2[1] + F3[1] + F4[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1], k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            Fr = [F3[0] + F4[0] + F5[0] + F6[0] + F7[0], F3[1] + F4[1] + F5[1] + F6[1] + F7[1]]

                    if i == len(M) - 1:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1], k)
                            Fr = [F1[0] + F7[0] + F8[0], F1[1] + F7[1] + F8[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1], k)
                            Fr = [F1[0] + F5[0] + F6[0] + F7[0] + F8[0], F1[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            Fr = [F5[0] + F6[0] + F7[0], F5[1] + F6[1] + F7[1]]

                    F[i][j] = Fr


            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0])):
                    if i == 0:

                        if j == 0:
                            if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
                            if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j + 1] = distance_entre(M[i + 1][j + 1], M[i][j])
                            if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])

                        if j != 0 and j != len(M[0]) - 1:
                            if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
                            if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j + 1] = distance_entre(M[i + 1][j + 1], M[i][j])
                            if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])
                            if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j - 1] = distance_entre(M[i + 1][j - 1], M[i][j])
                            if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])

                        if j == len(M[0]) - 1:
                            if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])
                            if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j - 1] = distance_entre(M[i + 1][j - 1], M[i][j])
                            if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])

                    if i != 0 and i != len(M) - 1:

                        if j == 0:
                            if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
                            if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j + 1] = distance_entre(M[i + 1][j + 1], M[i][j])
                            if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])
                            if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])
                            if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j + 1] = distance_entre(M[i - 1][j + 1], M[i][j])

                        if j != 0 and j != len(M[0]) - 1:
                            if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
                            if np.absolute(deformation([i + 1,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j + 1] = distance_entre(M[i + 1][j + 1], M[i][j])
                            if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])
                            if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j - 1] = distance_entre(M[i + 1][j - 1], M[i][j])
                            if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])
                            if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j - 1] = distance_entre(M[i - 1][j - 1], M[i][j])
                            if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])
                            if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j + 1] = distance_entre(M[i - 1][j + 1], M[i][j])

                        if j == len(M[0]) - 1:
                            if np.absolute(deformation([i + 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j] = distance_entre(M[i + 1][j], M[i][j])
                            if np.absolute(deformation([i + 1,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i + 1][j - 1] = distance_entre(M[i + 1][j - 1], M[i][j])
                            if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])
                            if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j - 1] = distance_entre(M[i - 1][j - 1], M[i][j])
                            if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])

                    if i == len(M) - 1:

                        if j == 0:
                            if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
                            if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])
                            if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j + 1] = distance_entre(M[i - 1][j + 1], M[i][j])

                        if j != 0 and j != len(M[0]) - 1:
                            if np.absolute(deformation([i,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j + 1] = distance_entre(M[i][j + 1], M[i][j])
                            if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])
                            if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j - 1] = distance_entre(M[i - 1][j - 1], M[i][j])
                            if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])
                            if np.absolute(deformation([i - 1,j + 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j + 1] = distance_entre(M[i - 1][j + 1], M[i][j])

                        if j == len(M[0]) - 1:
                            if np.absolute(deformation([i,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i][j - 1] = distance_entre(M[i][j - 1], M[i][j])
                            if np.absolute(deformation([i - 1,j - 1], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j - 1] = distance_entre(M[i - 1][j - 1], M[i][j])
                            if np.absolute(deformation([i - 1,j], [i,j])) > limite_delasticite:
                                liaisons[i][j][i - 1][j] = distance_entre(M[i - 1][j], M[i][j])


                    if i == len(M)-1 and j == len(M[0])-1 and q<0:
                        force_horizontale = 10
                        force_verticale = 10

                    if i == len(M)-1 and j == len(M[0])-2 and q<0:
                        force_horizontale = -5.5
                        force_verticale = -5.5

                    else:
                        force_horizontale = 0
                        force_verticale = 0
            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0])):

                    ACC[i][j][0] = (F[i][j][0] - alpha * V[i][j][0] + force_horizontale) / m
                    ACC[i][j][1] = (F[i][j][1] - alpha * V[i][j][1] + poids + force_verticale) / m

                    M[i][j][0] = M[i][j][0] + V[i][j][0] * dt + dt ** 2 / 2 * ACC[i][j][0]
                    M[i][j][1] = M[i][j][1] + V[i][j][1] * dt + dt ** 2 / 2 * ACC[i][j][1]


            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0])):
                    if i == 0:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1], k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            Fr = [F1[0] + F2[0] + F3[0], F1[1] + F2[1] + F3[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1], k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1], k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0], F1[1] + F2[1] + F3[1] + F4[1] + F5[1]]

                        if j == len(M[0]) - 1:
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1], k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            Fr = [F3[0] + F4[0] + F5[0], F3[1] + F4[1] + F5[1]]

                    if i != 0 and i != len(M) - 1:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1], k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1], k)
                            Fr = [F1[0] + F2[0] + F3[0] + F7[0] + F8[0], F1[1] + F2[1] + F3[1] + F7[1] + F8[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], liaisons[i][j][i + 1][j + 1], k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1], k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1], k)
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0] + F6[0] + F7[0] + F8[0],
                                  F1[1] + F2[1] + F3[1] + F4[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F3 = force_ressort(M[i + 1][j], M[i][j], liaisons[i][j][i + 1][j], k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], liaisons[i][j][i + 1][j - 1], k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            Fr = [F3[0] + F4[0] + F5[0] + F6[0] + F7[0], F3[1] + F4[1] + F5[1] + F6[1] + F7[1]]

                    if i == len(M) - 1:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1], k)
                            Fr = [F1[0] + F7[0] + F8[0], F1[1] + F7[1] + F8[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], liaisons[i][j][i][j + 1], k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], liaisons[i][j][i - 1][j + 1], k)
                            Fr = [F1[0] + F5[0] + F6[0] + F7[0] + F8[0], F1[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F5 = force_ressort(M[i][j - 1], M[i][j], liaisons[i][j][i][j - 1], k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], liaisons[i][j][i - 1][j - 1], k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], liaisons[i][j][i - 1][j], k)
                            Fr = [F5[0] + F6[0] + F7[0], F5[1] + F6[1] + F7[1]]

                    F[i][j] = Fr

                    if i == len(M)-1 and j == len(M[0])-1 and q<0 :
                        force_horizontale = -5
                        force_verticale = -5

                    else:
                        force_horizontale = 0
                        force_verticale = 0

            for i in range(fixer_1er_ligne_x, len(M)):
                for j in range(fixer_1er_ligne_y, len(M[0])):

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

            end_time=time.time()

            frame_calculation_time=end_time-start_time

            if number_of_frames % (0.02/dt) == 0:
                canvas.delete("all")
                dessine_lignes(M)
                dessine_les_points_de_la_matrice(M)


            number_of_frames+=1
            print(number_of_frames*dt)


            window.update()

        window.mainloop()

# care=rectangle(1/10,10000,0.5,1,[1,0.2],1,[0.2,1],[[0,0,0,0]],[0,0],np.pi/6) #longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/700,300)#temps_de_la_simulation,precision_dt,scale

# care=rectangle(1/3,50,0.5,1,[1,1],1,[0.7,1],[[0,0,0,0]],[0,0],np.pi/6)#longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/200,300)#temps_de_la_simulation,precision_dt,scale

# care=rectangle(1/2,500,0.5,1,[1,1],1,[0.7,0],[[1,1,0.5,0]],[0,0],0)#longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/1000,300)#temps_de_la_simulation,precision_dt,scale

# care=rectangle(0.02,100000,0.2,1,[1,0.05],1,[0.2,1],[[0,0,0,0]],[0,0],0)#longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
# care.simuler(10000,1/10000,600)#temps_de_la_simulation,precision_dt,scale

care=rectangle(1/10,1000,0.5,1,[1,0.2],1,[0.2,1],[[0,0,0,0]],[0,0],np.pi/6) #longueur_precision_spaciale,raideur,dissipation_lors_des_collision,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G,rotat
care.simuler(10000,1/1000,300)#temps_de_la_simulation,precision_dt,scale




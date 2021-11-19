import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import *

# maintenant on commencera le codage de la simulation en 2D d'un objet rectangle à plusieurs particules qui sera defini
# simplement par les données de ses points qui se trouvent á ses extrimités, on commencera l'algorithme par implementer
# juste les forces de ressort et puis apres on definira les forces internes tq les forces inter particules qui aiderons
# á empecher l'objet de s'effondre sur lui meme, puis un peut plus tard on ajoutera les collisions qui rendrons la
# simulation plus reele, mais ce qui sera plus impressionnant est l'ajout des phase d'elasticité et de plasticité pour
# les materiaux, chose que je n'est pas encore y pensé une solution mais on vera!!!


def matrice(y, x):
    F = []
    for k in range(0, y):
        L = []
        for l in range(0, x):
            s = '.'
            L.append(s)
        F.append(L)
    return F


class rectangle:
    def __init__(self, longueur_precision_spaciale, raideur, mass, dimensions, alpha, position_initial, positions_de_qlq_points, vitesse_de_G):
        self.len = longueur_precision_spaciale
        self.stif = raideur
        self.dim = dimensions
        self.mass = mass
        self.position = position_initial
        self.start = positions_de_qlq_points
        self.alpha = alpha
        self.vit = vitesse_de_G

    def simuler(self, temps_de_la_simulation, precision_dt, scale):
        t = temps_de_la_simulation
        dt = precision_dt
        s = scale

        alpha = self.alpha
        l = self.len
        d = l*np.sqrt(2)
        k = self.stif
        a = np.floor(self.dim[0]/l)*l
        b = np.floor(self.dim[1]/l)*l
        x = self.position[0]
        y = self.position[1]
        g = 9.81

        # M est la matrice representant les points du solide

        M = []
        V = []
        ACC = []
        F = []
        nombre_de_points = 0
        for i in range(0, int(b/l)):
            L = []
            K = []
            I = []
            T = []
            for j in range(0, int(a/l)):
                nombre_de_points += 1
                L.append([x + l * j, y + l * i])
                K.append(self.vit)
                I.append([0, 0])
                T.append([0, 0])
            M.append(L)
            V.append(K)
            ACC.append(I)
            F.append(T)

        m = self.mass/nombre_de_points

        # maintenant on reorganise quelque points suivant les commande de positions_de_qlq_points

        for o in self.start:
            i = o[0]
            j = o[1]
            M[i][j] = [x+o[2]*l, y+o[3]*l]
            print(M[i][j])

        W = 800
        H = 500
        window = Tk()
        canvas = Canvas(window, width=W, height=H, bg="grey")
        canvas.pack()

        def dessine_point(A):
            canvas.create_rectangle(
                A[0]*s-1, H-A[1]*s+1, A[0]*s+2, H-A[1]*s-2, fill="black")

        def dessine_les_points_de_la_matrice(M):
            for i in M:
                for p in i:
                    dessine_point(p)

        def dessine_ligne_entre(A, B):
            canvas.create_line(A[0]*s, H-A[1]*s, B[0]*s, H-B[1]*s, fill="red")

        def A(L, i, j):  # une fonction qui aidera á bien organiser les points de la matrice
            return L[i][j]

        def dessine_lignes(M):
            for i in range(0, len(M)):
                for j in range(0, len(M[0])):
                    if i != len(M)-1:

                        if j == 0:

                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j))
                            dessine_ligne_entre(A(M, i, j), A(M, i, j + 1))
                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j + 1))

                        if j != 0 and j != len(M[0])-1:

                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j))
                            dessine_ligne_entre(A(M, i, j), A(M, i, j + 1))
                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j + 1))
                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j - 1))

                        if j == len(M[0])-1:

                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j))
                            dessine_ligne_entre(A(M, i, j), A(M, i + 1, j - 1))

                    if i == len(M)-1:
                        if j != len(M[0])-1:

                            dessine_ligne_entre(A(M, i, j), A(M, i, j + 1))

        dessine_lignes(M)
        dessine_les_points_de_la_matrice(M)

        # force appliquée par le ressort se situant entre B et A sur A
        def force_ressort(B, A, l, k):
            Ax = A[0]
            Ay = A[1]
            Bx = B[0]
            By = B[1]
            AB = np.sqrt((Bx - Ax) ** 2 + (By - Ay) ** 2)
            return [k * (l - AB) * (Ax - Bx) / AB,  k * (l - AB) * (Ay - By) / AB]

        for l in range(0, int(t*50/dt)):
            for i in range(1, len(M)):
                for j in range(0, len(M[0])):
                    if i == 0:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], d, k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            Fr = [F1[0] + F2[0] + F3[0], F1[1] + F2[1] + F3[1]]

                        if j != 0 and j != len(M[0])-1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], d, k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], d, k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0],
                                  F1[1] + F2[1] + F3[1] + F4[1] + F5[1]]

                        if j == len(M[0])-1:
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], d, k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            Fr = [F3[0] + F4[0] + F5[0], F3[1] + F4[1] + F5[1]]

                    if i != 0 and i != len(M)-1:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], d, k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], d, k)
                            Fr = [F1[0] + F2[0] + F3[0] + F7[0] + F8[0],
                                  F1[1] + F2[1] + F3[1] + F7[1] + F8[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], d, k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], d, k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], d, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], d, k)
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0] + F6[0] + F7[0] + F8[0],
                                  F1[1] + F2[1] + F3[1] + F4[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], d, k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], d, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            Fr = [F3[0] + F4[0] + F5[0] + F6[0] + F7[0],
                                  F3[1] + F4[1] + F5[1] + F6[1] + F7[1]]

                    if i == len(M)-1:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], d, k)
                            Fr = [F1[0] + F7[0] + F8[0], F1[1] + F7[1] + F8[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], d, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], d, k)
                            Fr = [F1[0] + F5[0] + F6[0] + F7[0] + F8[0],
                                  F1[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], d, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            Fr = [F5[0] + F6[0] + F7[0], F5[1] + F6[1] + F7[1]]

                    F[i][j] = Fr

            for i in range(1, len(M)):
                for j in range(0, len(M[0])):
                    if i == 0:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], d, k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            Fr = [F1[0] + F2[0] + F3[0], F1[1] + F2[1] + F3[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], d, k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], d, k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0],
                                  F1[1] + F2[1] + F3[1] + F4[1] + F5[1]]

                        if j == len(M[0]) - 1:
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], d, k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            Fr = [F3[0] + F4[0] + F5[0], F3[1] + F4[1] + F5[1]]

                    if i != 0 and i != len(M) - 1:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], d, k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], d, k)
                            Fr = [F1[0] + F2[0] + F3[0] + F7[0] + F8[0],
                                  F1[1] + F2[1] + F3[1] + F7[1] + F8[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F2 = force_ressort(M[i + 1][j + 1], M[i][j], d, k)
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], d, k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], d, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], d, k)
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0] + F6[0] + F7[0] + F8[0],
                                  F1[1] + F2[1] + F3[1] + F4[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F3 = force_ressort(M[i + 1][j], M[i][j], l, k)
                            F4 = force_ressort(M[i + 1][j - 1], M[i][j], d, k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], d, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            Fr = [F3[0] + F4[0] + F5[0] + F6[0] + F7[0],
                                  F3[1] + F4[1] + F5[1] + F6[1] + F7[1]]

                    if i == len(M) - 1:

                        if j == 0:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], d, k)
                            Fr = [F1[0] + F7[0] + F8[0], F1[1] + F7[1] + F8[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(M[i][j + 1], M[i][j], l, k)
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], d, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            F8 = force_ressort(M[i - 1][j + 1], M[i][j], d, k)
                            Fr = [F1[0] + F5[0] + F6[0] + F7[0] + F8[0],
                                  F1[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F5 = force_ressort(M[i][j - 1], M[i][j], l, k)
                            F6 = force_ressort(M[i - 1][j - 1], M[i][j], d, k)
                            F7 = force_ressort(M[i - 1][j], M[i][j], l, k)
                            Fr = [F5[0] + F6[0] + F7[0], F5[1] + F6[1] + F7[1]]

                    F[i][j] = Fr

            for i in range(1, len(M)):
                for j in range(0, len(M[0])):

                    acc_Aij_x_1 = (F[i][j][0] - alpha * V[i][j][0]) * dt / m
                    acc_Aij_y_1 = (F[i][j][1] - alpha * V[i][j][1]) * dt / m

                    acc_Aij_x_0 = ACC[i][j][0]
                    acc_Aij_y_0 = ACC[i][j][1]

                    V[i][j][0] = V[i][j][0] + dt / \
                        2 * (acc_Aij_x_1 + acc_Aij_x_0)
                    V[i][j][1] = V[i][j][1] + dt / \
                        2 * (acc_Aij_y_1 + acc_Aij_y_0)

            canvas.delete("all")
            dessine_lignes(M)
            dessine_les_points_de_la_matrice(M)

            window.update()

        window.mainloop()


# longueur_precision_spaciale,raideur,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G
care = rectangle(0.4, 100, 10, [1, 1], 10, [0.2, 0.2], [[0, 0, 0, 0]], [0, 0])
care.simuler(10, 1/500, 300)  # temps_de_la_simulation,precision_dt,scale

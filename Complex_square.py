import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import *


class simple_square:
    def __init__(self,length,stiffness,dimensions,mass,start):
        self.len= length
        self.k=stiffness
        self.dim=dimensions
        self.mass=mass
        self.start=start

    def simulate(self,t,alpha,scale,accuracy):
        def SPRING_FORCE(B,A,l,k):
            Ax = A[0]
            Ay = A[1]
            Bx = B[0]
            By = B[1]
            AB=np.sqrt((Bx - Ax) ** 2 + (By - Ay) ** 2)
            return [ k*(l - AB)*(Ax - Bx)/AB,  k * ((l/AB) - 1)*(Ay - By)/AB]
        l=self.len
        d=l*np.sqrt(2)
        k=self.k
        g=9.81
        s=scale
        m=self.mass
        a=self.dim[0]
        b=self.dim[1]
        dt=accuracy
        A=self.start[0]
        B=self.start[1]
        C=self.start[2]
        D=self.start[3]
        #les coordonnees de A à t'=t+dt
        W = 800
        H = 500
        window = Tk()
        canvas = Canvas(window, width=W, height=H, bg="grey")
        canvas.pack()
        ground = canvas.create_rectangle(0,300,800,310)
        pointA = canvas.create_rectangle(A[0]*s, A[1]*s,(A[0]+a)*s  + 1, (A[1]+b)*s + 1, fill="pink")
        pointB = canvas.create_rectangle(B[0]*s, B[1]*s,(B[0]+a)*s  + 1, (B[1]+b)*s + 1, fill="blue")

        pointC = canvas.create_rectangle(C[0]*s, 300-C[1]*s,(C[0]+a)*s  + 1, 300-(C[1]+b)*s + 1, fill="black")
        pointD = canvas.create_rectangle(D[0]*s, 300-D[1]*s,(D[0]+a)*s  + 1, 300-(D[1]+b)*s + 1, fill="black")

        lineAB = canvas.create_line(A[0] * s + a / 2, 300-a-A[1] * s + a / 2, B[0] * s + a / 2,300-a- B[1] * s + a / 2, fill='red')
        lineAC = canvas.create_line(A[0] * s + a / 2, 300-a-A[1] * s + a / 2, C[0] * s + a / 2,300-a- C[1] * s + a / 2, fill='red')
        lineAD = canvas.create_line(A[0] * s + a / 2, 300-a-A[1] * s + a / 2, D[0] * s + a / 2,300-a- D[1] * s + a / 2, fill='red')
        lineBC = canvas.create_line(B[0] * s + a / 2, 300-a-B[1] * s + a / 2, C[0] * s + a / 2,300-a- C[1] * s + a / 2, fill='red')
        lineDB = canvas.create_line(D[0] * s + a / 2, 300-a-D[1] * s + a / 2, B[0] * s + a / 2,300-a- B[1] * s + a / 2, fill='red')
        lineDC = canvas.create_line(D[0] * s + a / 2, 300-a-D[1] * s + a / 2, C[0] * s + a / 2,300-a- C[1] * s + a / 2, fill='red')

        time.sleep(1)
        Avx1=0
        Ax1=A[0]
        Avy1=0
        Ay1=A[1]
        Bvx1=0
        Bx1=B[0]
        Bvy1=0
        By1=B[1]
        for i in range(0, int(t * 50/dt)):
            FBA=SPRING_FORCE(B,A,l,k)
            FCA=SPRING_FORCE(C,A,l,k)
            FDA=SPRING_FORCE(D,A,d,k)
            FAB=SPRING_FORCE(A,B,l,k)
            FDB=SPRING_FORCE(D,B,l,k)
            FCB=SPRING_FORCE(C,B,d,k)
            #FAC=SPRING_FORCE(A,C,l,k)
            #FDC=SPRING_FORCE(D,C,l,k)
            #FBC=SPRING_FORCE(B,C,d,k)
            #FAD=SPRING_FORCE(A,D,d,k)
            #FBD=SPRING_FORCE(B,D,l,k)
            #FCD=SPRING_FORCE(C,D,l,k)
            #if i==0:
                #Ax1 = (dt ** 2 / m)*(FBA[0] + FCA[0] + FDA[0]) + A[0]
                #Ay1 = (dt ** 2 / m)*(FBA[1] + FCA[1] + FDA[1] - m * g) + A[1]
                #Bx1 = (dt ** 2 / m)*(FAB[0] + FCB[0] + FDB[0]) + B[0]
                #By1 = (dt ** 2 / m)*(FAB[1] + FCB[1] + FDB[1] - m * g) + B[1]
                #canvas.moveto(pointA, np.floor(Ax1 * scale), 500 - a - np.floor(Ay1 * scale))
                #canvas.moveto(pointB, np.floor(Bx1 * scale), 500 - a - np.floor(By1 * scale))
                #canvas.moveto(pointA, np.floor(Ax1 * scale), 500 - a - np.floor(Ay1 * scale))
            Avx1 += (FBA[0] + FCA[0] + FDA[0] - alpha * Avx1) * dt / m
            Ax1 += Avx1 * dt
            Avy1 += (FBA[1] + FCA[1] + FDA[1] - m * g - alpha * Avy1) * dt / m
            Ay1 += Avy1 * dt
            Bvx1 += (FAB[0] + FCB[0] + FDB[0] - alpha * Bvx1) * dt / m
            Bx1 += Bvx1 * dt
            Bvy1 += (FAB[1] + FCB[1] + FDB[1] - m * g - alpha * Bvy1) * dt / m
            By1 += Bvy1 * dt

            A[0]=Ax1
            A[1]=Ay1
            B[0]=Bx1
            B[1]=By1


                #Ax2 = (dt ** 2 / (m - alpha*dt))*(FBA[0] + FCA[0] + FDA[0] + alpha * Ax1 / dt - A[0]/(dt**2))
                #Ay2 = (dt ** 2 / (m - alpha*dt))*(FBA[1] + FCA[1] + FDA[1] + alpha * Ay1 / dt - A[1]/(dt**2) - m * g)
                #Bx2 = (dt ** 2 / (m - alpha*dt))*(FAB[0] + FCB[0] + FDB[0] + alpha * Bx1 / dt - B[0]/(dt**2))
                #By2 = (dt ** 2 / (m - alpha*dt))*(FAB[1] + FCB[1] + FDB[1] + alpha * By1 / dt - B[1]/(dt**2) - m * g)
                #Cx1 = (dt ** 2 / (m - alpha))(FAC[0] + FBC[0] + FDC[0] + alpha * Cx / dt)
                #Cy1 = (dt ** 2 / (m - alpha))(FAC[1] + FBC[1] + FDC[1] + alpha * Cy / dt-mg)
                #Dx1 = (dt ** 2 / (m - alpha))(FAD[0] + FBD[0] + FCD[0] + alpha * Dx / dt)
                #Dy1 = (dt ** 2 / (m - alpha))(FAD[1] + FBD[1] + FCD[1] + alpha * Dy / dt-mg)

            canvas.delete(lineAB)
            canvas.delete(lineAC)
            canvas.delete(lineAD)
            canvas.delete(lineBC)
            canvas.delete(lineDB)

            lineAB = canvas.create_line(A[0] * s + a , 300 - a - A[1] * s , B[0] * s , 300 - a - B[1] * s , fill='red')
            lineAC = canvas.create_line(A[0] * s + a , 300 - a - A[1] * s , C[0] * s , 300 - a - C[1] * s , fill='red')
            lineAD = canvas.create_line(A[0] * s + a , 300 - a - A[1] * s , D[0] * s , 300 - a - D[1] * s , fill='red')
            lineBC = canvas.create_line(B[0] * s + a , 300 - a - B[1] * s , C[0] * s , 300 - a - C[1] * s , fill='red')
            lineDB = canvas.create_line(D[0] * s + a , 300 - a - D[1] * s , B[0] * s , 300 - a - B[1] * s , fill='red')

            canvas.moveto(pointA, np.floor(Ax1 * scale), 300-a-np.floor(Ay1 * scale))
            canvas.moveto(pointB, np.floor(Bx1 * scale), 300-a-np.floor(By1 * scale))

            window.update()
            time.sleep(0.02*dt)
            print(canvas.coords(pointA))
            print(FBA[0],FBA[1],FAB[0],FAB[1])
            A=[Ax1,Ay1]
            B=[Bx1,By1]


        window.mainloop()



#cube=osci(2,1,[70,70],10,[3,0])
#cube.oscillate_display(10,1,100)
#cube=simple_square(1,2,[0.1,0.1],0.2,[[1.7,1.4],[2,1],[1,0],[2,0]])
#cube.simulate(10,10,100,1/50)


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

        #M est la matrice representant les points du solide

        M = []
        V = []
        ACC = []
        nombre_de_points=0
        for i in range(0,int(b/l)):
            L=[]
            K=[]
            I=[]
            for j in range(0,int(a/l)):
                nombre_de_points+=1
                L.append([x+l*j,y+l*i])
                K.append(self.vit)
                I.append([0,0])
            M.append(L)
            V.append(K)
            ACC.append(I)

        m = self.mass/nombre_de_points

        #maintenant on reorganise quelque points suivant les commande de positions_de_qlq_points

        for o in self.start:
            i=o[0]
            j=o[1]
            M[i][j]=[x+o[2]*l,y+o[3]*l]
            print(M[i][j])

        W = 800
        H = 500
        window = Tk()
        canvas = Canvas(window, width=W, height=H, bg="grey")
        canvas.pack()

        def dessine_point(A):
            canvas.create_rectangle(A[0]*s-1,A[1]*s+1,A[0]*s+2,A[1]*s-2,fill="black")

        def dessine_les_points_de_la_matrice(M):
            for i in M:
                for p in i:
                    dessine_point(p)

        def dessine_ligne_entre(A,B):
            canvas.create_line(A[0]*s,A[1]*s,B[0]*s,B[1]*s,fill="red")

        def A(L,i,j): #une fonction qui aidera á bien organiser les points de la matrice
            return L[i][j]

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

        M1=M

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

                    acc_Aij_x_0 = (Fr[0] - alpha * V[i][j][0]) * dt / m
                    acc_Aij_y_0 = (Fr[1] - alpha * V[i][j][1]) * dt / m

                    ACC[i][j][0] = acc_Aij_x_0
                    ACC[i][j][1] = acc_Aij_y_0

                    M1[i][j][0] = M[i][j][0] + V[i][j][0] * dt + dt ** 2 / 2 * acc_Aij_x_0
                    M1[i][j][1] = M[i][j][1] + V[i][j][1] * dt + dt ** 2 / 2 * acc_Aij_y_0

            M=M1
            V1=V
            for i in range(0, len(M)):
                for j in range(0, len(M[0])):
                    if i == 0:

                        if j == 0:
                            F1 = force_ressort(A(M, i, j + 1), A(M, i, j), l, k)
                            F2 = force_ressort(A(M, i + 1, j), A(M, i, j), l, k)
                            F3 = force_ressort(A(M, i + 1, j + 1), A(M, i, j), d, k)
                            Fr = [F1[0] + F2[0] + F3[0], F1[1] + F2[1] + F3[1]]

                        if j != 0 and j != len(M[0]) - 1:
                            F1 = force_ressort(A(M, i, j + 1), A(M, i, j), l, k)
                            F2 = force_ressort(A(M, i + 1, j), A(M, i, j), l, k)
                            F3 = force_ressort(A(M, i + 1, j + 1), A(M, i, j), d, k)
                            F4 = force_ressort(A(M, i, j - 1), A(M, i, j), l, k)
                            F5 = force_ressort(A(M, i + 1, j - 1), A(M, i, j), d, k)
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0], F1[1] + F2[1] + F3[1] + F4[1] + F5[1]]

                        if j == len(M[0]) - 1:
                            F2 = force_ressort(A(M, i + 1, j), A(M, i, j), l, k)
                            F4 = force_ressort(A(M, i, j - 1), A(M, i, j), l, k)
                            F5 = force_ressort(A(M, i + 1, j - 1), A(M, i, j), d, k)
                            Fr = [F4[0] + F2[0] + F5[0], F4[1] + F2[1] + F5[1]]

                    if i != 0 and i != len(M) - 1:

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
                            Fr = [F1[0] + F2[0] + F3[0] + F4[0] + F5[0] + F6[0] + F7[0] + F8[0],
                                  F1[1] + F2[1] + F3[1] + F4[1] + F5[1] + F6[1] + F7[1] + F8[1]]

                        if j == len(M[0]) - 1:
                            F2 = force_ressort(A(M, i + 1, j), A(M, i, j), l, k)
                            F4 = force_ressort(A(M, i, j - 1), A(M, i, j), l, k)
                            F5 = force_ressort(A(M, i + 1, j - 1), A(M, i, j), d, k)
                            F7 = force_ressort(A(M, i - 1, j), A(M, i, j), l, k)
                            F8 = force_ressort(A(M, i - 1, j - 1), A(M, i, j), d, k)
                            Fr = [F4[0] + F2[0] + F5[0] + F7[0] + F8[0], F4[1] + F2[1] + F5[1] + F7[1] + F8[1]]

                    if i == len(M) - 1:

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

                    acc_Aij_x_1 = (Fr[0] - alpha * V[i][j][0]) * dt / m
                    acc_Aij_y_1 = (Fr[1] - alpha * V[i][j][1]) * dt / m

                    acc_Aij_x_0 = ACC[i][j][0]
                    acc_Aij_y_0 = ACC[i][j][1]

                    V1[i][j][0] = V[i][j][0] + dt / 2 * (acc_Aij_x_1 + acc_Aij_x_0)
                    V1[i][j][1] = V[i][j][1] + dt / 2 * (acc_Aij_y_1 + acc_Aij_y_0)

                    M1[i][j][0] = M[i][j][0] + V[i][j][0] * dt + dt ** 2 / 2 * acc_Aij_x_0
                    M1[i][j][1] = M[i][j][1] + V[i][j][1] * dt + dt ** 2 / 2 * acc_Aij_y_0

            M=M1





                    #V[i][j] = [V[i][j][0] + (Fr[0] - alpha * V[i][j][0]) * dt / m, V[i][j][1] + (Fr[1] - alpha * V[i][j][1]) * dt / m]
                    #M[i][j] = [M[i][j][0] + V[i][j][0] * dt, M[i][j][1] + V[i][j][1] * dt]

            canvas.delete("all")
            dessine_lignes(M)
            dessine_les_points_de_la_matrice(M)

            window.update()
            time.sleep(0.02)

        window.mainloop()

care=rectangle(0.3,1,10,[1,1],1,[1,1],[[0,0,-0.1,-0.1]],[0,0])#longueur_precision_spaciale,raideur,mass,dimensions,alpha,position_initial,positions_de_qlq_points,vitesse_de_G
care.simuler(10,1/50,100)#temps_de_la_simulation,precision_dt,scale

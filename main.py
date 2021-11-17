//Je suis trop beau
import numpy as np
import matplotlib.pyplot as plt
import time
from tkinter import *


class osci:
    def __init__(self, lenght, stiffness, dimensions, mass, start):
        self.len = lenght
        self.k = stiffness
        self.dim = dimensions
        self.mass = mass
        self.start = start
    def oscillate_display(self,t,alpha,scale):

        l=self.len
        m=self.mass
        k=self.k
        x0=self.start[0]
        v0=self.start[1]
        a=self.dim[0]
        b=self.dim[1]
        delta = alpha ** 2 / m ** 2 - 4 * np.sqrt(k / m)
        if delta<0:
            def x(t):
                A = x0 - l
                B = v0 + alpha / (2 * m) * A
                omega = np.sqrt(-delta / 4)
                return (np.exp(-alpha/(2*m)*t)*(A*np.cos(t*omega)+B*np.sin(t*omega))+l)
        if delta>0:
            def x(t):
                r1 = -alpha / (2 * m) - np.sqrt(delta)
                r2 = -alpha / (2 * m) + np.sqrt(delta)
                B = (v0 + r1 * (l - x0)) / (r2 - r1)
                A = x0 - l - B
                return (A*np.exp(r1*t)+B*np.exp(r2*t)+l)
        if delta==0:
            def x(t):
                r0 = -alpha / (2 * m)
                A=x0-l
                B=v0-r0*A
                return (np.exp(r0*t)*(A+B*t)+l)


        W = 800
        H = 500
        window = Tk()
        canvas = Canvas(window,width=W,height=H,bg="grey")
        canvas.pack()
        rectangle=canvas.create_rectangle(x0*scale, 500-b, x0*scale+a, 500, fill="black")
        for i in range(0,t*50):
            s=int(np.floor(x(i/10)*scale))
            canvas.moveto(rectangle,s,500-b)
            window.update()
            time.sleep(0.02)
            print(canvas.coords(rectangle))

        window.mainloop()
        Lt = np.linspace(0, t, 1000)
        Lx = x(Lt)
        plt.figure(num=0, dpi=120)
        plt.plot(Lt, Lx)
        plt.show()

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
cube=simple_square(1,2,[0.1,0.1],0.2,[[1.7,1.4],[2,1],[1,0],[2,0]])
cube.simulate(10,10,100,1/50)

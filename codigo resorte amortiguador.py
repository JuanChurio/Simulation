import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from matplotlib import pyplot as plt
import numpy as np
from math import *


class const:
    def __init__(self):
        self.k=0
        self.c=0
        self.opc=0
        self.opc1=0
        self.Fa=0
        self.nt=0
        self.p=0
    def critico(self):
        h=0.06
        h1=0.1
        k1=18
        c1=7.1
        a=True
        while(a):
            c1=c1+h
            k1=k1-h1
            n=2*sqrt(2*k1)
            if (abs(c1-n)<=0.01):
                self.c=c1
                self.k=k1
                #print("k=",k,c)
                a=False  
    def sobre(self):
        h=0.06    
        h1=0.1
        k1=28
        c1=9.1
        a=True
        i=0
        while(a):
            c1=c1+h
            k1=k1-h1
            i=i+1
            n=2*sqrt(2*k1)
            if ((c1-n)>= 8):
                self.c=c1
                self.k=k1
                a=False           
    def sub(self):
        h=0.06
        h1=0.1
        k1=13
        c1=1
        a=True
        while(a):
            c1=c1+h
            k1=k1-h1
            n=2*sqrt(2*k1)
            if (n > c1):
                self.c=c1
                self.k=k1
                a=False       
ob=const()   
def lines():
    glBegin(GL_LINE_STRIP) # y = -0.3644x + 0.244
    glColor3f(255, 255, 255)
    glVertex2f(-0.5,-2.4)
    glVertex2f(0.5,-2.4)
    glEnd()  
def resorte(y):
    glBegin(GL_LINE_STRIP) # y = -0.3644x + 0.244
    glColor3f(0, 0, 255)
    glVertex2f(-0.05,-2.4)
    glVertex2f(-0.05,y-2.1)
    glEnd()
def amortiguador(y):
    glColor3f(255, 0, 0)
    glBegin(GL_LINE_STRIP) # y = -0.3644x + 0.244
    glVertex2f(0.05,-2.4)
    glVertex2f(0.05,y-2.1)
    glEnd()   
def square(xC,yC,mag):
    glColor3f(255, 255, 255)
    glBegin(GL_QUADS)
    glVertex2f(xC + mag,yC + mag)
    glVertex2f(xC - mag,yC + mag)
    glVertex2f(xC - mag,yC - mag)
    glVertex2f(xC+mag,yC-mag)
    glEnd()  
    
def f1(t,y,vy):
 f1= vy 
 return f1

    
def f2(t,y,vy,tm):
 m=2
 #impulso u
 if(ob.opc1==1):
     if(tm <= 0.1):
         ob.Fa = 5
     else:
         ob.Fa = 0 
#escalon u
 if(ob.opc1==2):
     if(tm >= 0.1):
         ob.Fa = 5
     else:
         ob.Fa = 0 
#rampa u
 if(ob.opc1==3):
     if(tm >= 0.1):
         ob.Fa = tm
     else:
         ob.Fa = 0  
 #fuerza especial 
 if(ob.opc1==4):
     print("valor de p= ",ob.p)  
     if(ob.p<=50):
         ob.Fa=0
     elif(ob.p>50 and ob.p<=101):
         ob.Fa=5
     if(ob.p==101):    
         ob.p=1   
 print("valor de p= ",ob.p)        
 f2= (-ob.c*vy-ob.k*y+ob.Fa)/m
 return f2

def rugecritico(ti,yi,vyi,h,opc):  
    py=[]
    ty=[]
    eq=True
    ob.p=0
    print("opciov",ob.opc1)
    print("tiempo ingres",ob.nt)
    while(eq):
        #posición en y
        ob.p=ob.p+1
        py.append(yi)
        t=ti
        ty.append(t)
        print("c=",ob.c,"k=",ob.k)
        k1y=f1(ti,yi,vyi)
        k1v=f2(ti,yi,vyi,t)
        k2y=f1(ti+h/2,yi+h*k1y/2,vyi+h*k1v/2)
        k2v=f2(ti+h/2,yi+h*k1y/2,vyi+h*k1v/2,t)
        k3y=f1(ti+h/2,yi+h*k2y/2,vyi+h*k2v/2)
        k3v=f2(ti+h/2,yi+h*k2y/2,vyi+h*k2v/2,t)
        k4y=f1(ti+h,yi+h*k3y,vyi+h*k3v)
        k4v=f2(ti+h,yi+h*k3y,vyi+h*k3v,t)
        y=yi+h/6*(k1y+2*k2y+2*k3y+k4y)
        vy=vyi+h/6*(k1v+2*k2v+2*k3v+k4v)
        vyi=vy
        yi=y
        print("y=",y,"v=",vy,"fuerza=",ob.Fa,"t=",ti)
        print("_______________________________________________________________________")
        print("")
        ti=ti+h
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #Limpia la ventana
        square(0,yi-2,0.1)
        lines()
        resorte(yi)
        amortiguador(yi)
        pygame.display.flip() #Solo la parte del buffer que se modifica se actualiza
        pygame.time.wait(100) #Espera 10 milisegundos
        #critico
        #print("tiempo",ti)
        for event in pygame.event.get(): #Para el caso de cerrar la ventana
            if event.type == pygame.QUIT:
                eq=False
                
        if(ob.opc1==4):
            if(opc==1):
                if(t>ob.nt):
                    eq=False
            #sub
            elif(opc==3):
                if(t>ob.nt):
                    eq=False
            #sobre       
            elif(opc==2):
                if(t>ob.nt):
                    eq=False   
        else:
            if(opc==1):
                if(t>10):
                    eq=False
        #sub
            elif(opc==3):
                if(t>10):
                    eq=False
        #sobre       
            elif(opc==2):
                if(t>10):
                    eq=False   
                
    plt.plot(ty,py)
    if(opc==1):
        plt.title('Vibraciones Criticamente amortiguadas')
    elif(opc==2):
        plt.title('Vibraciones sobre-amortiguadas')
    elif(opc==3):
        plt.title('Vibraciones sub-amortiguadas')
    plt.grid()
    pygame.quit()
    plt.show()
    return vyi,yi
   
def menu():
    print("------------------------------------------------------------")
    print("Se recomienda cerrar la terminal despues de ver la grafica.")
    print("------------------------------------------------------------")
    print("Digite la opción a visualizar")
    print("1.Impulso unitario")
    print("2.Escalon Unitario")
    print("3.Rampa unitaria")
    print("4.Fuerza especial")
    opc1=int(input())
    
    
    if(opc1 == 1):
        ob.opc1=opc1 
        print("Digite la opción a visualizar")
        print("1.Criticamente Amortiguado")
        print("2.Sobre-amortiguado")
        print("3.Sub-amortiguado")
        opc=int(input())
        #critico
        if(opc == 1):
            ob.critico()
            ob.opc=opc 
        #sobre
        elif(opc == 2):
            ob.sobre()
            ob.opc=opc   
        #sub
        elif(opc == 3):
            ob.sub()
            ob.opc=opc 
    #sobre
    elif(opc1 == 2):
        ob.opc1=opc1 
        print("Digite la opción a visualizar")
        print("1.Criticamente Amortiguado")
        print("2.Sobre-amortiguado")
        print("3.Sub-amortiguado")
        opc=int(input())
        #critico
        if(opc == 1):
            ob.critico()
            ob.opc=opc 
        #sobre
        elif(opc == 2):
            ob.sobre()
            ob.opc=opc   
        #sub
        elif(opc == 3):
            ob.sub()
            ob.opc=opc   
    #sub
    elif(opc1 == 3):
        ob.opc1=opc1 
        print("Digite la opción a visualizar")
        print("1.Criticamente Amortiguado")
        print("2.Sobre-amortiguado")
        print("3.Sub-amortiguado")
        opc=int(input())
        #critico
        if(opc == 1):
            ob.critico()
            ob.opc=opc 
        #sobre
        elif(opc == 2):
            ob.sobre()
            ob.opc=opc   
        #sub
        elif(opc == 3):
            ob.sub()
            ob.opc=opc 
            
    elif(opc1 == 4):
        tn=0
        ob.opc1=opc1 
        print("Digite el tiempo de ejecución")
        tn=int(input())
        ob.nt=tn
        print("_____________________________")
        print("Digite la opción a visualizar")
        print("1.Criticamente Amortiguado")
        print("2.Sobre-amortiguado")
        print("3.Sub-amortiguado")
        opc=int(input())
        #critico
        if(opc == 1):
            ob.critico()
            ob.opc=opc 
        #sobre
        elif(opc == 2):
            ob.sobre()
            ob.opc=opc   
        #sub
        elif(opc == 3):
            ob.sub()
            ob.opc=opc 
   
                         
def main():
    menu()
    pygame.init() #Inicializa pygame
    display = (800,700) #tamaño de la entana
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL) #Un display con bordes en -1,-1 y 1,1
    gluOrtho2D(-1,2,1,-2.5) 
    pc=ob.opc
    h=0.1
    yi=0.1
    vyi=0.1
    t=0
    xaprox,yaprox=rugecritico(t,yi,vyi,h,pc)  
    
main()
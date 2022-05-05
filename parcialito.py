from tkinter.tix import Tree
from turtle import position
import pygame

from pygame.locals import *
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

class Scene:
    def __init__(self,temp_sphereList,hexagon):
        self.sphereList = temp_sphereList
        self.hexagon = hexagon
    
    def drawScene(self):
        #Asintotas x=-0.3,x=0.3,y=-0.8
        self.Al = Lines((0.6,10),(0.6,-0.8))
        self.Bl = Lines((-0.6,10),(-0.6,-0.6))
        self.Cl = Lines((0.6,-0.8),(-0.4,-0.8))
        self.Dl = Lines((-0.4,-0.8),(-0.6,-0.6))
        
        self.listSides = [self.Al,self.Bl,self.Cl,self.Dl]
        self.coordinates = [[(-10,10),(-10,10),(-0.4,0.6),(-1,1)],[(-10,10),(-10,10),(-1,1),(-1,1)]]
        
        

    def moveScene(self,t,t_):
        self.hexagon.draw()
        for i in range(0,len(self.sphereList)):#Numero de esferas

            for j in range(0,4):#Numero de lados del escenario

                self.sphereList[i].impactLine(self.listSides[j],self.coordinates[0][j],self.coordinates[1][j])
                
                if(self.sphereList[i].impactLine(self.Dl,(-1,1),(-1,1))):
                    
                    self.sphereList[i].vx  += 1 
                    self.sphereList[i].vyo += 1 
                    

            for j in range(1,len(self.sphereList[i:])): #Choque entre pelotas
                
                if(self.sphereList[i].impactPoint(self.sphereList[i:][j]) and self.sphereList[i].active(t_) and self.sphereList[i:][j].active(t_)  ):
                    try:
                        temp_V =self.sphereList[i].linear_momentum(self.sphereList[i:][j],0.9)

                        self.sphereList[i:][j].vx  = temp_V[0]
                        self.sphereList[i:][j].vyo = temp_V[1]

                        if(self.sphereList[i].position[0] < self.sphereList[i:][j].position[0]):
                            self.sphereList[i].position[0]     -= 0.001
                            self.sphereList[i:][j].position[0] += 0.001

                        else:
                            self.sphereList[i].position[0]     += 0.001
                            self.sphereList[i:][j].position[0] -= 0.001

                        if(self.sphereList[i].position[1] < self.sphereList[i:][j].position[1]):
                            self.sphereList[i].position[1]     -= 0.001
                            self.sphereList[i:][j].position[1] += 0.001

                        else:
                            self.sphereList[i].position[1]     += 0.001
                            self.sphereList[i:][j].position[1] -= 0.001

                    except:
                        pass 

            if(self.sphereList[i].impactPoint(self.hexagon) and self.sphereList[i].active(t_)): #choque hexagono pelota
                v = self.sphereList[i].linear_momentum(self.hexagon,0.97)

                self.hexagon.vx = v[0]
                self.hexagon.impulse(self.sphereList[i],t)
                if(self.sphereList[i].position[0] < self.hexagon.position[0]):
                    self.sphereList[i].position[0]     -= 0.001
                    self.hexagon.position[0] += 0.001

                else:
                    self.sphereList[i].position[0]     += 0.001
                    self.hexagon.position[0] -= 0.001


            if(self.sphereList[i].active(t_)):
                self.sphereList[i].move(t)

        self.hexagon.impactLine(self.Al)
        self.hexagon.impactLine(self.Bl)
        self.hexagon.moveHex(t)      

class Hexagon:
    def __init__(self,magnitude):
        self.magnitude = magnitude
        self.position = [0,0]
        self.radious = magnitude + 0.001
        self.acceleration = 0
        self.vx = 0
        self.v = 0
        self.vyo = 0
        self.mass = 0.6
        self.kinetic = 0.1
        self.stactic = 0.3

    def moveHex(self,t):
        
        if(np.abs(self.vx) <= 0.02):
            self.acceleration = 0
            self.vx = 0
        self.v = -self.acceleration*t + self.vx
        self.vx = self.v
        temp_y = 0
        temp_x = self.v*t+self.position[0]
        self.position = [temp_x,temp_y]
        

    def impulse(self,objeto,t):
        
        self.acceleration=-0.98*self.kinetic*t+self.vx
        
    def minimumForce(self,object):
        vx=self.object.vx
        vy=self.object.vyo
        alpha=np.arctan(vy/vx)
        #fuerza de la esfera
        fsphere=self.f_apli=self.Sphere.a*self.Sphere.mass
        fsphere = object.acceleration*object.mass
        #fuerza necesaria para mover el hexagono 
        f=(self.mass*9.8*self.stactic)/(sin(alpha)*self.stactic-cos(alpha))
        if(fsphere>f):
            return True
        else:
            return False
        
        


    def draw(self):

        self.a = (self.magnitude+self.position[0],0)
        self.b = (self.magnitude*np.cos((np.pi/3))+self.position[0],self.magnitude*np.sin(np.pi/3))
        self.c = (-self.magnitude*np.cos((np.pi/3))+self.position[0],self.magnitude*np.sin(np.pi/3))
        self.d = (-self.magnitude+self.position[0],0)
        self.e = (-self.magnitude*np.cos((np.pi/3))+self.position[0],-self.magnitude*np.sin(np.pi/3))
        self.f = (self.magnitude*np.cos((np.pi/3))+self.position[0],-self.magnitude*np.sin(np.pi/3))
        
 
        self.Al = Lines(self.a,self.b)
        self.Bl = Lines(self.b,self.c)
        self.Cl = Lines(self.d,self.c)
        self.Dl = Lines(self.d,self.e)
        self.El = Lines(self.e,self.f)
        self.Fl = Lines(self.f,self.a)
        
        self.listSides = [self.Al,self.Bl,self.Cl,self.Dl,self.El,self.Fl]
        self.coordinates = [[(self.b[0],self.a[0]), (self.c[0],self.b[0]), (self.d[0],self.c[0]), (self.d[0],self.e[0]),(self.e[0],self.f[0]),(self.f[0],self.a[0])],
        [(self.b[1],self.a[1]),(-1,1),(self.c[1],self.d[1]),(self.d[1],self.c[1]),(-1,1),(self.f[1],self.a[1])]]
        
    def distanceLine(self,line):
        
        distance = np.abs( line[1]*self.position[0] + line[2])/pow(pow(line[0],2)+pow(line[1],2),0.5)
        return distance

    def impactLine(self,line):
        if(self.distanceLine(line) <= self.radious):
            self.vx = -0.97*self.vx
            self.acceleration = -self.acceleration
            return True
        return False
    


    def drawC(self):
        circle(self.position[0],self.position[1],self.radious)



class Sphere:
    def __init__(self,num,magnitude):
        self.num = num
        self.a = 0
        self.mass = 0.2
        self.radious = 0.06
        self.position = [-0.5,0.8]
        self.vx = magnitude*cos(radians(30))
        self.vyo = magnitude*sin(radians(30))
        
    def move(self,t):

        self.vy = -0.98*t + self.vyo
        self.vyo = self.vy
        temp_y = self.vy*t+self.position[1]
        temp_x = self.vx*t+self.position[0]
        self.position = [temp_x,temp_y]
        self.draw()

    def active(self,t_):
        
        if(self.num <= t_):
            return True
        return False
    

    def showValue(self):
        print(f"vy: {self.vy},vx: {self.vx},y: {self.position[1]},x: {self.position[0]} ")


    def rotationMatrixLine(self,line):
        theta = 0
        magnitude = [self.vx,self.vy]
        #magnitude = np.linalg.norm(magnitude)
        if(line[1]!=1 and line[1]!=0):
            theta =abs((np.arctan(line[1])))
            vp =  magnitude[0]*np.cos(theta) + magnitude[1]*np.sin(theta)
            vn = -magnitude[0]*np.sin(theta) + magnitude[1]*np.cos(theta)
            vp_n=((0.2-0.97)/0.2)*vp
            #segunda rotaciÃ³n
            self.vx = (vp_n*np.cos(theta)- vn*np.sin(theta))*0.2
            self.vyo =(vp_n*np.sin(theta) + vn*np.cos(theta))*0.2

            self.position[0] += 0.01
            self.position[1] += 0.01
        if(line[0] == 0):
            
            self.vx = -self.vx
            self.position[0] += (self.vx/np.abs(self.vx))*0.01
            
        if(line[1] == 0):
            
            self.vyo = -self.vy*0.97
            self.position[1] += (self.vyo/np.abs(self.vyo))*0.01
            
    def linear_momentum(self,objeto,e):
        
        m = (objeto.position[1]-self.position[1])/(objeto.position[0]-self.position[0])
        theta = np.arctan(m)

        ##
        vp2 = self.vx*np.cos(theta)+self.vyo*np.sin(theta)
        vn2 = -self.vx*np.sin(theta) + self.vyo*np.cos(theta)
        ##
        vp = objeto.vx*np.cos(theta) + objeto.vyo*np.sin(theta)
        vn = -objeto.vx*np.sin(theta) + objeto.vyo*np.cos(theta)
        ##
        v1p = ((objeto.mass-e*self.mass)/(objeto.mass+self.mass))*vp+(((1+e)*self.mass)/(objeto.mass+self.mass))*vp2
        v2p = (((1+e)*objeto.mass)/(self.mass+objeto.mass))*vp + ((self.mass-e*objeto.mass)/(self.mass+objeto.mass))*vp2
        ##
        vx =  v1p*np.cos(theta) - vn*np.sin(theta)
        vyo =  v1p*np.sin(theta) + vn*np.cos(theta)
        ##
        self.vx  =  (v2p*np.cos(theta) - vn2*np.sin(theta))
        self.vyo =  v2p*np.sin(theta) + vn2*np.cos(theta)
        
        return [vx,vyo]


    def draw(self):
        n=0
        glBegin(GL_LINE_STRIP)
        nSides=14
        while n<=nSides:
            angle=2*np.pi*n/nSides
            x=self.position[0]+self.radious*np.cos(angle)
            y=self.position[1]+self.radious*np.sin(angle)
            glVertex2f(x,y)
            n=n+1
        glEnd()

    

    def distancePoint(self,objeto):
        distance = pow(pow(self.position[0]-objeto.position[0],2)+pow(self.position[1]-objeto.position[1],2),0.5)
        return distance
        
    def impactPoint(self,objeto):
        if(self.distancePoint(objeto) <= self.radious+objeto.radious):
            return True
        return False

    def distanceLine(self,line):
        try:
            distance = np.abs( -line[1]*self.position[0] + line[0]*self.position[1] - line[2])/pow(pow(line[0],2)+pow(line[1],2),0.5)
        except:
            distance = 100
        return distance

    def impactLine(self,line,x,y):
        if(self.distanceLine(line) <= self.radious and   x[0] - self.radious   < self.position[0]  and self.position[0] < x[1] + self.radious and self.position[1]-self.radious > y[0] and self.position[1] < y[1] +self.radious ):
            self.rotationMatrixLine(line)
            return True
        return False


def Lines(point1,point2):
    glBegin(GL_LINE_STRIP)
    glVertex2fv(point1)
    glVertex2fv(point2)
    glEnd()
    try:
        y = 1
        m = (point2[1]-point1[1])/(point2[0]-point1[0])
        b = -m*point1[0]+point1[1]
    except:
        y = 0 
        m = 1
        b = -point1[0]
    return [y,m,b]


def circle(xCenter,yCenter, radius): #Gener un cÃ­rculo
    n=0
    glBegin(GL_LINE_STRIP)
    nSides=20
    while n<=nSides:
        angle=2*np.pi*n/nSides
        x=xCenter+radius*np.cos(angle)
        y=yCenter+radius*np.sin(angle)
        glVertex2f(x, y)
        n=n+1
    glEnd()


def main():
    myHexagon = Hexagon(0.12)
    mySphere =  Sphere(0,1)
    mySphere2 = Sphere(0.5,1)
    mySphere3 = Sphere(1.0,1)
    mySphere4 = Sphere(1.5,1)
    mySphere5 = Sphere(2.0,1)
    mySphere6 = Sphere(2.5,1)

    myScene = Scene([mySphere,mySphere2,mySphere3,mySphere4,mySphere5,mySphere6],myHexagon)
    t  = 0.001
    t_ = 0.001
    pygame.init() #Inicializa pygame
    display = (800,800) #tamaÃ±o de la entana
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL) #Un display con bordes en -1,-1 y 1,1
    
    while (True): #Ciclo infinito de funcionamiento
        for event in pygame.event.get(): #Para el caso de cerrar la ventana
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #Limpia la ventana
        ##
        
        
        myScene.drawScene()
        myScene.moveScene(t,t_)
        #mySphere.move(t)
        ''' mySphere2.move(t)
        mySphere3.move(t) '''
        #myHexagon.moveHex(t)
        #Condicionales de movimiento individual
        
        print("tiempo de ejecucion= ",t_)
        
        
        pygame.display.flip() #Solo la parte del buffer que se modifica se actualiza
        pygame.time.wait(1) #Espera 10 milisegundos
        t_ += 0.001
        #Cierra while True
  
main()
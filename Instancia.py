# ************************************************
#   Instancia.py
#   Define a classe Instancia
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************

from math import floor
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *

""" Classe Instancia """
class Instancia:   
    def __init__(self, nome):
        self.position = Ponto (0,0,0) 
        self.escala = Ponto (1,1,1)
        self.rotation:float = 0.0
        self.movement = Ponto(0,1,0)
        self.speed = 0.5
        self.colors = []
        self.max = Ponto (0,0,0)
        self.min = Ponto (0,0,0)
        self.columnsOffset = 0
        self.linesOffset = 0
        self.t = 0.0
        self.modelo = self.criaPersonagem(nome)
    
    def Desenha(self):
        glPushMatrix()
        glTranslatef(self.position.x, self.position.y, 0)
        glRotatef(self.rotation, 0, 0, 1)
        glScalef(self.escala.x, self.escala.y, self.escala.z)
        self.DesenhaPersonagem()
        glPopMatrix()
        
    def DesenhaPixel(self):
        glBegin(GL_QUADS)
        glVertex2f(-1, -1)
        glVertex2f(-1, 0)
        glVertex2f(0, 0)
        glVertex2f(0, -1)
        glEnd()
    
    def criaPersonagem(self, nome):
        #TODO: get max and min valuesss
        Nome = nome
        infile = open(Nome)
        line = infile.readline()
        number = int(line)
        for i in range(number):
            self.colors += [infile.readline().split()[1:]]
        [lines, columns] = infile.readline().split()
        lines, columns = (int(lines), int(columns))
        self.linesOffset = floor(lines/2)
        self.columnsOffset = floor(columns/2)
        aux = infile.readlines()
        infile.close()
        return [x.split() for x in aux]

    def DesenhaPersonagem(self):
        for line in range(len(self.modelo)):
            for column in range(len(self.modelo[line])):
                color = self.colors[int(self.modelo[line][column]) - 1]
                glColor3f(int(color[0])/255, int(color[1])/255, int(color[2])/255)
                posX = self.columnsOffset - column
                posY = self.linesOffset - line
                glPushMatrix()
                glTranslatef(posX, posY, 0)
                self.DesenhaPixel()
                glPopMatrix()
    

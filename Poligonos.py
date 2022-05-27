# ************************************************
#   Poligonos.py
#   Define a classe Polygon
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *
import copy


class Modelos:

    def __init__(self):
        self.Pixels = [] # atributo do objeto

    def getNPixels(self):
        return len(self.Pixels)
    
    def inserePixel(self, x, y, z):
        self.Pixels += [Ponto(x,y,z)]

    def getVertice(self, i):
        return self.Pixels[i]
    
    def desenhaPoligono(self):
        #print ("Desenha Poligono - Tamanho:", len(self.Vertices))
        glBegin(GL_LINE_LOOP)
        for V in self.Pixels:
            glVertex3f(V.x,V.y,V.z)
        glEnd();

    def desenhaVertices(self):
        glBegin(GL_POINTS);
        for V in self.Pixels:
            glVertex3f(V.x,V.y,V.z)
        glEnd();

    def imprimeVertices(self):
        for x in self.Pixels:
            x.imprime()

    def getLimits(self):
        Min = copy.deepcopy(self.Pixels[0])
        Max = copy.deepcopy(self.Pixels[0])
        
        for V in self.Pixels:
            if V.x > Max.x:
                Max.x = V.x
            if V.y > Max.y:
                Max.y = V.y
            if V.z > Max.z:
                Max.z = V.z
            if V.x < Min.x:
                Min.x = V.x
            if V.y < Min.y:
                Min.y = V.y
            if V.z < Min.z:
                Min.z = V.z
        #print("getLimits")
        #Min.imprime()
        #Max.imprime()
        return Min, Max
#def setColor()
# ***********************************************************************************
# LePontosDeArquivo(Nome):
#  Realiza a leitura de um arquivo com as coordenadas do polígono
# ***********************************************************************************
    def LePontosDeArquivo(self, Nome):
        
        Pt = Ponto()
        infile = open(Nome)
        line = infile.readline()
        number = int(line)
        for line in infile:
            #print ("Linha: ", line)
            words = line.split() # Separa as palavras na linha
            x = float (words[0])
            y = float (words[1])
            self.insereVertice(x,y,0)
            #Mapa.insereVertice(*map(float,line.split))
        infile.close()
        
        #print ("Após leitura do arquivo:")
        #Min.imprime()
        #Max.imprime()
        return self.getLimits()

    def getAresta(self, n):
        P1 = self.Pixels[n]
        n1 = (n+1) % self.getNPixels()
        P2 = self.Pixels[n1]
        return P1, P2

    def desenhaAresta(self, n):
        glBegin(GL_LINES)
        glVertex3f(self.Pixels[n].x,self.Pixels[n].y,self.Pixels[n].z)
        n1 = (n+1) % self.getNPixels()
        glVertex3f(self.Pixels[n1].x,self.Pixels[n1].y,self.Pixels[n1].z)
        glEnd()
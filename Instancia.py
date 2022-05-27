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
    def __init__(self, modelo):
        self.posicao = Ponto (0,0,0) 
        self.escala = Ponto (1,1,1)
        self.rotacao:float = 0.0
        self.modelo = modelo
        self.max = Ponto (0,0,0)
        self.min = Ponto (0,0,0)
        self.t = 0.0
    
    """ Imprime os valores de cada eixo do ponto """
    # Faz a impressao usando sobrecarga de funcao
    # https://www.educative.io/edpresso/what-is-method-overloading-in-python
    def imprime(self, msg=None):
        if msg is not None:
            pass 
        else:
            print ("Rotacao:", self.rotacao)

    """ Define o modelo a ser usada para a desenhar """
    def setModelo(self, func):
        self.modelo = func

    def Desenha(self):
        glPushMatrix();
        glTranslatef(self.posicao.x, self.posicao.y, 0)
        glRotatef(self.rotacao, 0, 0, 1)
        glScalef(self.escala.x, self.escala.y, self.escala.z)
        self.modelo()
        glPopMatrix()
        
    
        def criaPersonagem(self):
            Nome = "personagem.txt"
            Pt = Ponto()
            infile = open(Nome)
            line = infile.readline()
            number = int(line)
            colors = {}
            for i in range(number):
                colors[i] = infile.readline().split()[1:]
            [lines, columns] = infile.readline().split()
            lines, columns = (int(lines), int(columns))
            #todo: self-it down here
            linesOffset = floor(lines/2)
            columnsOffset = floor(columns/2)
            aux = infile.readlines()
            return [x.split() for x in aux]

    

# ***********************************************************************************
#   ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe uma curva de Bezier em OpenGL
#   Este programa cria um conjunto de INSTANCIAS
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# ***********************************************************************************

from math import floor
from random import random
from time import sleep
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *
from Instancia import *

# ***********************************************************************************

# Vida do jogador
vidas = 3

##TODO: jogador perde vida qndo é acertado:
##- um inimigo
##- um projetil


# Modelos de Objetos
personagem = Modelos()

modelos = ["MeiaSeta.txt", "Mastro.txt"]

# ***********************************************************************************
# Pontos de controle de uma curva Bezier
Curva1 = []

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()

# Quantidade de inimigos no universo
qtdInimigos = 2

# lista de instancias do universo
Universo = [] 

def DesenhaLinha (P1, P2):
    glBegin(GL_LINES)
    glVertex3f(P1.x,P1.y,P1.z)
    glVertex3f(P2.x,P2.y,P2.z)
    glEnd()

# ****************************************************************
def RotacionaAoRedorDeUmPonto(alfa: float, P: Ponto):
    glTranslatef(P.x, P.y, P.z)
    glRotatef(alfa, 0,0,1)
    glTranslatef(-P.x, -P.y, -P.z)

# **************************************************************
def CalculaBezier3(PC, t:float):
    P = Ponto()
    UmMenosT:float = 1-t;
    P =  PC[0] * UmMenosT * UmMenosT + PC[1] * 2 * UmMenosT * t + PC[2] * t*t;
    #P.imprime()
    return P

# ***********************************************************************************
def TracaBezier3Pontos():
    
    t=0.0
    DeltaT = 1.0/50
    P = Ponto;
    glBegin(GL_LINE_STRIP);
    
    while(t<1.0):
        P = CalculaBezier3(Curva1, t)
        glVertex2f(P.x, P.y)
        t += DeltaT
    P = CalculaBezier3(Curva1, 1.0) #faz o acabamento da curva
    glVertex2f(P.x, P.y)
    
    glEnd()

# ***********************************************************************************
def reshape(w,h):

    global Min, Max
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Selecão, com 10% das dimensoes do poligono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    #glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glOrtho(Min.x, Max.x, Min.y, Max.y, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def DesenhaPixel():
    glBegin(GL_QUADS);
    glVertex2f(-1, -1);
    glVertex2f(-1, 0);
    glVertex2f(0, 0);
    glVertex2f(0, -1);
    glEnd();
    
def DesenhaPersonagem():
    
    # print(matrix)
    # for line in range(lines):
        # for column in range(columns):
            # color = colors[int(matrix[line][column]) - 1]
            # glColor3f(int(color[0]), int(color[1]), int(color[2]));
            # posX = columnsOffset - column
            # posY = linesOffset - line
            # print(posX, posY)
            # glPushMatrix();
            # glTranslatef(posX, posY, 0);
            # DesenhaPixel();
            # glPopMatrix();
    # infile.close()
    
    #print ("Após leitura do arquivo:")
    #Min.imprime()
    #Max.imprime()
    return 0#self.getLimits()
    glPushMatrix();

    glTranslatef(2, 0, 0);
    glColor3f(1, 0, 0);
    DesenhaRetangulo();

    glTranslatef(0, 2, 0);
    glColor3f(0, 0, 1);
    DesenhaRetangulo();

    glTranslatef(-2, 0, 0);
    glColor3f(1, 1, 0);
    DesenhaRetangulo();
    glPopMatrix();
    pass


# **************************************************************
def DesenhaEixos():
    global Min, Max

    Meio = Ponto(); 
    Meio.x = (Max.x+Min.x)/2
    Meio.y = (Max.y+Min.y)/2
    Meio.z = (Max.z+Min.z)/2

    glBegin(GL_LINES)
    #  eixo horizontal
    glVertex2f(Min.x,Meio.y)
    glVertex2f(Max.x,Meio.y)
    #  eixo vertical
    glVertex2f(Meio.x,Min.y)
    glVertex2f(Meio.x,Max.y)
    glEnd()

# ***********************************************************************************
def DesenhaUniverso():
    for I in Universo:
        I.Desenha()

# ***********************************************************************************
def AtualizaUniverso():
    if Universo[0].t>1.0:
        Universo[0].t = 0.0
    else:
        DeltaT = 1.0/5000
        Universo[0].t += DeltaT
    P = CalculaBezier3(Curva1, Universo[0].t)
    Universo[0].posicao = P
    
# ***********************************************************************************
def display():
    
    #sleep(0.05)

	# Limpa a tela coma cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glLineWidth(3)
    glColor3f(1,1,1) # R, G, B  [0..1]
    DesenhaEixos()
    glColor3f(1,1,0)
    #AtualizaUniverso()
    DesenhaPersonagem()
    glColor3f(1,0,0)
    TracaBezier3Pontos()

    glutSwapBuffers()

# ***********************************************************************************
# The function called whenever a key is pressed. 
# Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
ESCAPE = b'\x1b'
def keyboard(*args):
    print (args)
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == ESCAPE:
        os._exit(0)
# Forca o redesenho da tela
    glutPostRedisplay()


# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        #TODO: andar para frente
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        #TODO: rotacionar para a esquerda
        pass
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        #TODO: rotacionar para a direita
        pass

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouse(button: int, state: int, x: int, y: int):
    global PontoClicado
    if (state != GLUT_DOWN): 
        return
    if (button != GLUT_RIGHT_BUTTON):
        return
    #print ("Mouse:", x, ",", y)
    # Converte a coordenada de tela para o sistema de coordenadas do 
    # universo definido pela glOrtho
    vport = glGetIntegerv(GL_VIEWPORT)
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    realY = vport[3] - y
    worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    PontoClicado = Ponto (worldCoordinate1[0],worldCoordinate1[1], worldCoordinate1[2])
    PontoClicado.imprime("Ponto Clicado:")

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************
def mouseMove(x: int, y: int):
    #glutPostRedisplay()
    return

def CarregaModelos():
    global MeiaSeta, Mastro
    MeiaSeta.LePontosDeArquivo("MeiaSeta.txt")
    Mastro.LePontosDeArquivo("Mastro.txt")
    

def CarregaModelo(pos):
    #TODO: Carrega modelo individualmente
    return Modelos().LePontosDeArquivo(modelos[pos])

# ***********************************************************************************
# Esta função deve instanciar todos os personagens do cenário
# ***********************************************************************************
def CriaInstancias():
    global Universo
    #personagem
    
    instacia = Instancia(matrix)
    #TODO: Fazer o instanciamento generico, loop com a quantidade total de modelos no universo, gerando os modelos com uma aleatoriedade
    # for i in range(qtdInimigos):
    #     Universo.append(Instancia())
    #     Universo[i].modelo = CarregaModelo(random() * len(modelos))

# ***********************************************************************************
def CriaCurvas():
    global Curva1
    Curva1 += [Ponto (-5,-5)]
    Curva1 += [Ponto (0,6)]
    Curva1 += [Ponto (5,-5)]

# ***********************************************************************************
def init():
    global Min, Max
    # Define a cor do fundo da tela (PRETA)
    glClearColor(29/255, 41/255, 81/255, 1)
    DesenhaPersonagem()
    #CarregaModelos()
    CriaCurvas()
    d:int = 20
    Min = Ponto(-d,-d)
    Max = Ponto(d,d)


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Animacao com Bezier")
glutDisplayFunc(display)
glutIdleFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
init()

try:
    glutMainLoop()
except SystemExit:
    pass

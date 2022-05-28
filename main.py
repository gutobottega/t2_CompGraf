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

from math import floor, cos, radians, sin
from random import random
from time import sleep
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Instancia import *

# ***********************************************************************************

# Vida do jogador
vidas = 3

#balas
balas = 10

##TODO: jogador perde vida qndo é acertado:
##- um inimigo
##- um projetil



modelos: list[str] = [
    "personagens/p1.txt",
    "personagens/p2.txt",
    "personagens/p3.txt",
    "personagens/p4.txt",
    "personagens/p5.txt",
    ]

# ***********************************************************************************
# Pontos de controle de uma curva Bezier
Curva1 = []

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()

# Quantidade de inimigos no universo
qtdInimigos = 5

personagem = Instancia('personagens/personagem.txt')

# lista de instancias do universo
inimigos:list[Instancia] = [] 

# lista de instancias do universo
tiros:list[Instancia] = [] 

# **************************************************************
def CalculaBezier3(PC, t:float):
    P = Ponto()
    UmMenosT:float = 1-t;
    P =  PC[0] * UmMenosT * UmMenosT + PC[1] * 2 * UmMenosT * t + PC[2] * t*t;
    #P.imprime()
    return P

# ***********************************************************************************
def TracaBezier3Pontos():
    
    t=1.0
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
    
def DesenhaPersonagem():
    personagem.Desenha()
    inimigos[0].position = Ponto(-30, 20, 0)
    inimigos[1].position = Ponto(-30, -20, 0)
    inimigos[2].position = Ponto(0, -20, 0)
    inimigos[3].position = Ponto(30, -20, 0)
    inimigos[4].position = Ponto(30, 20, 0)
    [x.Desenha() for x in inimigos]
 
def DesenhaTiros():
    [x.Desenha() for x in tiros]
    
def rotaciona(V:Ponto, angulo:float):
    angulo = radians(angulo)
    x = V.x * cos(angulo) - V.y * sin(angulo)
    y = V.x * sin(angulo) + V.y * cos(angulo)
    return Ponto(x, y)
    


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

def isVisible(pos):
    if(pos.x < Max.x and pos.x > Min.x):
            if(pos.y < Max.y and pos.y > Min.y):
                return True
    return False
# ***********************************************************************************
def AtualizaTiro():
    #tiros
    remove = []
    for i in range(len(tiros)):
        newPos = tiros[i].position + rotaciona(tiros[i].movement, tiros[i].rotation) * tiros[i].speed
        if(not isVisible(newPos)):
            remove += [i]
        else: tiros[i].position = newPos
    [tiros.pop(j) for j in remove]
    #TODO: translate tiros
    
def AtualizaUniverso():
    pass
    # if inimigos[0].t>1.0:
    #     inimigos[0].t = 0.0
    # else:
    #     DeltaT = 1.0/5000
    #     inimigos[0].t += DeltaT
    # P = CalculaBezier3(Curva1, inimigos[0].t)
    #Universo[0].position = P
    
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
    AtualizaTiro()
    DesenhaPersonagem()
    DesenhaTiros()
    glColor3f(1,0,0)
    TracaBezier3Pontos()

    glutSwapBuffers()
 
# ***********************************************************************************
# The function called whenever a key is pressed. 
# Note the use of Python tuples to pass in: (key, x, y)
#ESCAPE = '\033'
ESCAPE = b'\x1b'
def keyboard(*args):
    global tiros
    # If escape is pressed, kill everything.
    if args[0] == b'q':
        os._exit(0)
    if args[0] == b' ':
        #TODO: gerar uma instancia do tiro, no maximo 10
        if(len(tiros) + 1 <= balas):
            inst = Instancia('personagens/tiro.txt')
            inst.position = personagem.position
            inst.rotation = personagem.rotation
            tiros += [inst]
            inst.Desenha()
    if args[0] == ESCAPE:
        os._exit(0)
    glutPostRedisplay()


# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    global personagem
    personagem = personagem
    if a_keys == GLUT_KEY_UP:  
        newPos = personagem.position + rotaciona(personagem.movement, personagem.rotation)
        if(isVisible(newPos)):
            personagem.position = newPos
        
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        #TODO: rotacionar para a esquerda
        personagem.rotation += 10 
        
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        #TODO: rotacionar para a direita
        personagem.rotation -= 10
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
    

# ***********************************************************************************
# Esta função deve instanciar todos os personagens do cenário
# ***********************************************************************************
def CriaInstancias():
    global inimigos
    for i in range(qtdInimigos):
        #TODO:randomizar os inimigos
        inimigos.append(Instancia(modelos[i]))  

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
    CriaInstancias()
    CriaCurvas()
    d:int = 80
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
glutSpecialFunc(arrow_keys);
init()

try:
    glutMainLoop()
except SystemExit:
    pass

from sympy import *
##############################
######## Funções #############
##############################
def escalarXvetor(e, v):
    for i in range (0,len(v)):
        v[i] = e*v[i]
    return v

def somaVetor (v1, v2):
    resp = []
    for i in range(0, len(v1)):
        resp.append(v1[i] + v2[i])
    return resp

def kutta(yk, h, f):
    v1 = escalarXvetor(h, f)
    return somaVetor(yk, v1)

def f_vector(equacoes):    
    return 0

def solucao_inicial(vetor):
    
    for i in range (0,len(vetor)):
        yo.append(vetor[i])
    return yo

### Passos a,b, c e d da aula do dia 02_05_2019
def fa(t,yo):
    
    f1 = 100*yo[0] - 0.37*yo[0]*yo[1]
    f2 = -100*yo[1] + 0.05*yo[0]*yo[1]
    yFa = [f1,f2]
    return yFa

def fb(yo,h, yFa ):
    f1 = yo[0] + h/2 * yFa[0]
    f2 = yo[1] + h/2 * yFa[1]
    yFb = [f1,f2]
    return yFb

def fc(to,h):
    tc = to + h/2
    return tc

def fd(tc,yo,yFb,h):


    f1 = 100*yFb[0] - 0.37*yFb[0]*yFb[1]
    f2 = -100*yFb[1] + 0.05*yFb[0]*yFb[1]
    yFd = [f1,f2]

    return yFd


##############################
######## Programa ############
##############################

v1 = [1000, 300]
h = 0.002
v2 = [-5390.05, -14406.80]
    
#print (kutta(v1, h, v2))

#testeando F
t = 0
a = Symbol('y')
b = Symbol ('y')
x = Symbol('x')
y = Symbol ('y')
h = 0.002
y1 = 1000
y2 = 300
f1 = Eq(100*y , 0.37*y*x)
f2 = Eq(-100*x + 0.05*x*y)
#Exemplo usando a biblioteca Funções
eq = solve ([8*x - 5*y + 8  ,  2*x + 5*y],[x,y])
y0 = [y1,y2]
eqn = Eq(y*(8.0 - y**3), 8.0)
print (eqn)
print ()

#Passo A
yFA = fa(0,y0) 
print("\n ### Passo [A] ### \n " + str(yFA))

#Passo B
yFB = fb(y0,h,yFA) 
print("\n ### Passo [B] ### \n " + str(yFB))

#Passo C
tc = fc(t,h)
print("\n ### Passo [C] ### \n " + str(tc))

#Passo D
yFD = fd(tc,y0,yFB,h)
print("\n ### Passo [D] ### \n " + str(yFD) + "\n")

#Cáculo do RageKutta após D
rkt = somaVetor(escalarXvetor(h,yFD) , y0)
print("Y = "+str(rkt)+"\n")

### Equações do nosso trabalho ###
#dS/dt = −βSI  = -axy
#dI/dt = βSI − cI = axy - cy
#dR/dt = cI = cy
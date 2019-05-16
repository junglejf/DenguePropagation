from sympy import *
##############################
######## Funções #############
##############################
def escalarXvetor(e, v):
    for i in range (0,len(v)):
        v[i] = e*v[i]
    return v

def subvetor(v1,v2):
    resp = []
    for i in range (0,len(v1)):
        resp.append(v1[i]-v2[i])
    return resp

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

def f(t,yo,h):
    yFa = fa(t,yo)
    #print(yFa)
    yFb = fb(yo,h,yFa)
    #print(yFb)
    tc = fc(t,h) 
    #print(tc)
    yFd = fd(tc,yo,yFb,h)
    #print(yFd)
    return yFd

def kutta_exp (yk,h,f1,f0, y0):
    print(f1)
    y1 = escalarXvetor(3,f1)
    print(y1)
    y2 = subvetor(y1,f0)
    print(y2)
    y3 = escalarXvetor(h/2, y2)
    print(y3)
    yn = somaVetor(yk,y3)
    
    #kutta_exp(yn,h,f0,f(t,y0,h),y1)
    return yn

##############################
######## Programa ############
##############################

v1 = [1000, 300]
h = 0.002
v2 = [-5390.05, -14406.80]
    
#print (kutta(v1, h, v2))

#testeando F
t = 0
h = 0.002
y01 = 1000
y02 = 300
#Exemplo usando a biblioteca Funções
Y0 = [y01,y02]

#Passo A
yFA = fa(0,Y0) 
print("\n ### Passo [A] ### \n " + str(yFA))

#Passo B
yFB = fb(Y0,h,yFA) 
print("\n ### Passo [B] ### \n " + str(yFB))

#Passo C
tc = fc(t,h)
print("\n ### Passo [C] ### \n " + str(tc))

#Passo D
yFD = fd(tc,Y0,yFB,h)
print("\n ### Passo [D] ### \n " + str(yFD) + "\n")

#Cálculo do RageKutta Y1 após D
#Y1 = somaVetor(escalarXvetor(h,yFD) , y0)
f_vet = f(t,Y0,h)
Y1 = kutta(Y0,h,f_vet)
print("Kutta - Y1 = "+str(Y1)+"\n")

#Cálculo do RageKutta Y2 
#t = h
#f_vet2 = f(t,Y1,h)
#rkt3 = kutta(Y1,h,f_vet2)
#print("Kutta - Y2 = "+str(rkt3)+"\n")


# Cálculo do kutta explíctio
Y2 = kutta_exp (Y1,h,fa(t,Y1),fa(t,Y0), Y0)
print("Kutta Exp - Y2 = "+str(Y2)+"\n")

#rktExp = kutta_exp(Y0,h,Y1,Y0,Y0)
#print("KuttaExp - Y2 = "+ str(rktExp)+'\n')

### Equações do nosso trabalho ###
## - Modelo de 3a ordem - ##
#dS/dt = −βSI  = -axy
#dI/dt = βSI − cI = axy - cy
#dR/dt = cI = cy

## - Modelo de 2a ordem - ##
#dS/dt = −βSI + γI + μN − δS  = -bxy + a(x+y) + cx 
#dI/dt = βSI − γI − δI = bxy - ay - cy
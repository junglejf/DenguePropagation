##############################
##### Variaveis Globais ######
##############################

## Array de Coeficientes
# coeficientes = [β,γ,μ,δ]
# β é a taxa de contato entre suscetíveis e infectados
# γ é a taxa de recuperação
# μ é a taxa de natalidade
# δ é a taxa de mortalidade
coef = [10,20,300,-40]

##############################
######## Funcoes #############
##############################

##Funcao que multiplica um vetor por um escalar
def escalarXvetor(e, v):
    for i in range (0,len(v)):
        v[i] = e*v[i]
    return v

##Funcao que subtrai os valores de dois vetores
def subvetor(v1,v2):
    resp = []
    for i in range (0,len(v1)):
        resp.append(v1[i]-v2[i])
    return resp

##Funcao que soma os valores de dois vetores
def somaVetor (v1, v2):
    resp = []
    for i in range(0, len(v1)):
        resp.append(v1[i] + v2[i])
    return resp

##Funcao que resolve a multiplicacao de um vetor por um escalar e depois soma com outro vetor
def kutta(yk, h, f):
    v1 = escalarXvetor(h, f)
    return somaVetor(yk, v1)

## - Modelo de 2a ordem - Modelo SIS - suscetível, infectado e suscetível , página 36 ##
# f1 = dS/dt = −βSI + γI + μ(S+I) − δS  
# f2 = dI/dt = βSI − γI − δI  
# S é a população de indivíduos suscetíveis
# I é a população de indivíduos infectados

##Esta eh a funcao que define as funcoes do problema
def f(t,y):
    global coef 
    # coef = [β,γ,μ,δ]
    # y =[S,I]
    # Essa é a SIS
    f1 = -coef[0]*y[0]*y[1] + coef[1]*y[1] + coef[2]*(y[0] + y[1]) - coef[3]*y[0]
    f2 = coef[0]*y[0]*y[1] - coef[1]*y[1] - coef[3]*y[1]
    yFa = [f1,f2]
    return yFa


##Funcao que resolve o metodo de Range Kutta
def range_kutta(y, h, t):
    a = f(t, y)
    b = kutta(y, h/2, a)
    c = t + h/2
    d = f(c, b)
    return kutta(y, h, d)

#Metodo explicito.
#YK Atual, FK Atual, H, Y anterior, F anterior
def kutta_exp (yk, fk, h, y0, f0, t, x):
    if x <= 10:
        y1 = escalarXvetor(3,fk)
        y2 = subvetor(y1,f0)
        y3 = escalarXvetor(h/2, y2)
        yn = somaVetor(yk,y3)
        print("Y"+ str(x) + ":")
        print(yn)
        kutta_exp(yn, f(t, yn), h, yk, f(t,yk), t, x+1)
        

##############################
######## Programa ############
##############################

##Inicializacao das variaveis
t = 0
h = 0.002
y01 = 100
y02 = 30

Y0 = [y01,y02]


#Com um passo eu resolvo range Kutta de segunda ordem
Y1 = range_kutta(Y0, h, t)


print("Y0: ")
print(Y0)
print("Y1: ")
print(Y1)

#Metodo explicito! 
resp = kutta_exp(Y1, f(t, Y1), h, Y0, f(t, Y0), t, 2)

#!/usr/bin/python
# -*- coding: latin-1 -*-


import os

# LISTA DE EQUA��ES P�GINAS 44 E 45 (FALTA TERMINAR):

# d(Et)dt = coef[0] * [1 - (Et / C')] * Wt - (coef[1] + coef[4]) * Et        # P�gina 44, equa��o E(t)
#
# d(Lt)dt = coef[1] * Et - (coef[2] + coef[5] + coef[10]) * Lt        # P�gina 44, equa��o L(t)
#
# d(Pt)dt = coef[2] * Lt - (coef[3] + coef[6] + coef[11]) * Pt        # P�gina 44, equa��o P(t)
#
# d(W1t)dt = coef[3] * Pt - (coef[13] * (It / N) + coef[7] + coef[12]) * W1t        # P�gina 44, equa��o W1(t)
#
# d(W2t)dt = coef[13] * (It / N) * W1t - (coef[15] + coef[7] + coef[12]) * W2t        # P�gina 44, equa��o W2(t)
#
# d(W3t)dt = coef[15] * W2t - (coef[7] + coef[12]) * W3t        # P�gina 44, equa��o W3(t)
#
# d(st)dt = coef[19] * N - [coef[14] * (W3t / Wt) + coef[18]] * St        # P�gina 45, equa��o s(t)
#
# d(et)dt = coef[14] * (W3t / Wt) * St - (coef[16] + coef[18]) * Et        # P�gina 45, equa��o e(t)
#
# d(it)dt = coef[16] * Et - (coef[17] + coef[18]) * It        # P�gina 45, equa��o i(t)
#
# d(rt)dt = coef[17] * It - coef[18] * Rt        # P�gina 45, equa��o r(t)

# ATEN��O: F = Per�odo Favor�vel; D = Per�odo Desfavor�vel; I = Per�odo Intermedi�rio.
# Usei Per�odo Favor�vel em todas as equa��es que usavam Mortalidade Mosquito Alado (?w) = coef[7]
# P�gina 46, Tabela 1 (Tabela de par�metros)

# coef[0] = ? => Ovoposi��o
# coef[1] = ?e => Ovo ? Larva(F) ou Ovo ? Larva(D) ou Ovo ? Larva(I)
# coef[2] = ?l => Larva ? Pupa(F) ou Larva ? Pupa(D) ou Larva ? Pupa(I)
# coef[3] = ?p => Pupa ? Alado(F) ou Pupa ? Alado(D) ou Pupa ? Alado(I)
# coef[4] = ?e => Mortalidade de Ovo
# coef[5] = ?l => Mortalidade de Larva
# coef[6] = ?p => Mortalidade de Pupa
# coef[7] = ?w(F) => Mortalidade Mosquito Alado(F)
# coef[8] = ?w(D) => Mortalidade Mosquito Alado(D)
# coef[9] = ?w(I) => Mortalidade Mosquito Alado(I)
# coef[10] = ?'l => Mortalidade - Larvicida
# coef[11] = ?'p => Mortalidade - "Pupicida"
# coef[12] = ?'w => Mortalidade - Inseticida
# coef[13] = ?w => Transmiss�o Mosquito - Humano
# coef[14] = ?h => Transmiss�o Humano - Mosquito
# coef[15] = ?w => Mosquito exposto ? infectado
# coef[16] = ?h => Humano exposto ? infectado
# coef[17] = ?h => Humano Infectado ? Removido
# coef[18] = ?h => Mortalidade Humanos
# coef[19] = ?n => Natalidade Humanos


# ARRAY DE PAR�METROS COM OS VALORES EXTRA�DOS DA TABELA 1 DA P�GINA 46:
# coef = [1, 0.33, 0.3, 0.2, 0.14, 0.125, 0.066, 0.346, 0.323, 0.0091, 0.05, 0.05, 0.0167, 0.042, 0.04, 0.059, 0, 0, 0, 0.75, 0.375, 0.2, 0.1, 0.143, 0.000042], 0.00042



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
def remove_file():
    os.remove("valores.csv")

def write_file(a):
    f = open("valores.csv", "a")
    for i in range (0, len(a)-1):
        f.write(str(a[i]) + ';')
    f.write(str(a[len(a) -1]) + '\n')
    f.close()

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
    y1 = kutta(y, h, d)
    write_file(y1)
    return y1

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
        write_file(yn)
        kutta_exp(yn, f(t, yn), h, yk, f(t,yk), t, x+1)
        

##############################
######## Programa ############
##############################

remove_file()

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

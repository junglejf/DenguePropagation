#!/usr/bin/python
# -*- coding: latin-1 -*-


import os

# LISTA DE EQUAÇÕES PÁGINAS 44 E 45 (FALTA TERMINAR):

# d(Et)dt = coef[0] * [1 - (Et / C')] * Wt - (coef[1] + coef[4]) * Et        # Página 44, equação E(t)
#
# d(Lt)dt = coef[1] * Et - (coef[2] + coef[5] + coef[10]) * Lt        # Página 44, equação L(t)
#
# d(Pt)dt = coef[2] * Lt - (coef[3] + coef[6] + coef[11]) * Pt        # Página 44, equação P(t)
#
# d(W1t)dt = coef[3] * Pt - (coef[13] * (It / N) + coef[7] + coef[12]) * W1t        # Página 44, equação W1(t)
#
# d(W2t)dt = coef[13] * (It / N) * W1t - (coef[15] + coef[7] + coef[12]) * W2t        # Página 44, equação W2(t)
#
# d(W3t)dt = coef[15] * W2t - (coef[7] + coef[12]) * W3t        # Página 44, equação W3(t)
#
# d(st)dt = coef[19] * N - [coef[14] * (W3t / Wt) + coef[18]] * St        # Página 45, equação s(t)
#
# d(et)dt = coef[14] * (W3t / Wt) * St - (coef[16] + coef[18]) * Et        # Página 45, equação e(t)
#
# d(it)dt = coef[16] * Et - (coef[17] + coef[18]) * It        # Página 45, equação i(t)
#
# d(rt)dt = coef[17] * It - coef[18] * Rt        # Página 45, equação r(t)

# ATENÇÃO: F = Período Favorável; D = Período Desfavorável; I = Período Intermediário.
# Usei Período Favorável em todas as equações que usavam Mortalidade Mosquito Alado (?w) = coef[7]
# Página 46, Tabela 1 (Tabela de parâmetros)

# coef[0] = ? => Ovoposição
# coef[1] = ?e => Ovo ? Larva(F)
# coef[2] = ?l => Larva ? Pupa(F)
# coef[3] = ?p => Pupa ? Alado(F)
# coef[4] = ?e => Mortalidade de Ovo
# coef[5] = ?l => Mortalidade de Larva
# coef[6] = ?p => Mortalidade de Pupa
# coef[7] = ?w(F) => Mortalidade Mosquito Alado(F)
# coef[8] = ?w(D) => Mortalidade Mosquito Alado(D)
# coef[9] = ?w(I) => Mortalidade Mosquito Alado(I)
# coef[10] = ?'l => Mortalidade - Larvicida
# coef[11] = ?'p => Mortalidade - "Pupicida"
# coef[12] = ?'w => Mortalidade - Inseticida
# coef[13] = ?w => Transmissão Mosquito - Humano
# coef[14] = ?h => Transmissão Humano - Mosquito
# coef[15] = ?w => Mosquito exposto ? infectado
# coef[16] = ?h => Humano exposto ? infectado
# coef[17] = ?h => Humano Infectado ? Removido
# coef[18] = ?h => Mortalidade Humanos
# coef[19] = ?n => Natalidade Humanos


# ARRAY DE PARÂMETROS COM OS VALORES EXTRAÍDOS DA TABELA 1 DA PÁGINA 46:
coef = [1.0, 0.33, 0.14, 0.346, 0.05, 0.05, 0.0167, 0.042, 0.04, 0.059, 0.0, 0.0, 0.0, 0.75, 0.375, 0.2, 0.1, 0.143, 0.000042, 0.00042]


##############################
#Inicializacao das variaveis#
##############################


#Valores iniciais

t = 0
h = 0.02

Et = 100
Lt = 200
Pt = 300
W1t = 100
W2t = 100
W3t = 200
Wt = W1t + W2t + W3t
St = 2
It = 3 
Rt = 4

Y0 = [float(Et), float(Lt), float(Pt), float(W1t), float(W2t), float(W3t), float(Wt), float(St), float(It), float(Rt)]


Cfixo = 700.0     #Valor referente ao periodo favoravel
Ci = 0.00000044         #Valor do teorema do chute
Clinha = Cfixo * Ci     #capacidade de suporte ambiental

N = 500000.0 #Populacao humana


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

def f(t, y):
    print(t)
    f1 = coef[0] * (1.0 - (y[0] / Clinha)) * y[6]  - (coef[1] + coef[4]) * y[0]        # Página 44, equação E(t)
    f2 = coef[1] * y[0] - (coef[2] + coef[5] + coef[10]) * y[1]         # Página 44, equação L(t)
    f3 = coef[2] * y[1]  - (coef[3] + coef[6] + coef[11]) * y[2]         # Página 44, equação P(t)
    f4 = coef[3] * y[2] - (coef[13] * (y[8]  / N) + coef[7] + coef[12]) * y[3]         # Página 44, equação W1(t)
    f5 = coef[13] * (y[8]  / N) * y[3]  - (coef[15] + coef[7] + coef[12]) * y[4]         # Página 44, equação W2(t)
    f6 = coef[15] * y[4]  - (coef[7] + coef[12]) * y[5]         # Página 44, equação W3(t)
    f7 = coef[19] * N - (coef[14] * (y[5]  / y[6] ) + coef[18]) * y[7]        # Página 45, equação s(t)
    f8 = coef[14] * (y[5]  / y[6] ) * y[7]  - (coef[16] + coef[18]) * y[0]       # Página 45, equação e(t)
    f9 = coef[16] * y[0]  - (coef[17] + coef[18]) * y[8]         # Página 45, equação i(t)
    f10 = coef[17] * y[8]  - coef[18] * y[9]         # Página 45, equação r(t)
    yFa = [f1,f2, f3, f4, f5, f6, f7, f8, f9, f10]
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
        t = t+h
        kutta_exp(yn, f(t, yn), h, yk, f(t,yk), t, x+1)
        

##############################
######## Programa ############
##############################

remove_file()

#Com um passo eu resolvo range Kutta de segunda ordem
Y1 = range_kutta(Y0, h, t)

print("Y0: ")
print(Y0)
print("Y1: ")
print(Y1)

#Metodo explicito! 
resp = kutta_exp(Y1, f(t, Y1), h, Y0, f(t, Y0), t, 2)

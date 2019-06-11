#!/usr/bin/python
# -*- coding: latin-1 -*-

import matplotlib.pyplot as plt
import os

##############################
########## Fun��es ###########
##############################

# Fun��o respons�vel em deletar o arquivo 'valores.csv'
def remove_file():
    os.remove("valores.csv")

# Fun��o respons�vel em criar o arquivo 'valores.csv'
def write_file(a):
    f = open("valores.csv", "a")
    for i in range (0, len(a) - 1):
        f.write(str(a[i]) + ';')
    f.write(str(a[len(a) - 1]) + '\n')
    f.close()

# Multiplica��o de um vetor por um escalar
def escalarXvetor(e, v):
    for i in range (0, len(v)):
        v[i] = e * v[i]
    return v

# Adi��o de valores entre dois vetores
def somaVetor(v1, v2):
    resp = []
    for i in range(0, len(v1)):
        resp.append(v1[i] + v2[i])
    return resp

# Subtra��o de valores entre dois vetores
def subvetor(v1, v2):
    resp = []
    for i in range (0, len(v1)):
        resp.append(v1[i] - v2[i])
    return resp

# Fun��o que atualiza os coeficientes:
# 'Taxa de Desenvolvimento de um Ovo para uma Larva',
# 'Taxa de Desenvolvimento de uma Larva para uma Pupa',
# 'Taxa de Desenvolvimento de uma Pupa para um Alado',
# 'Taxa de Mortalidade de Mosquito Alado' e
# 'Capacidade de Suporte Ambiental'
#  de acordo com a �poca do ano.
def atualiza_coeficientes():
    global Cfixo
    global coef
    if (Cfixo == 700): # (F) Favor�vel
        coef[1] = 0.33
        coef[2] = 0.14
        coef[3] = 0.346
        coef[7] = 0.042
    elif (Cfixo == 500): # (I) Intermedi�rio
        coef[1] = 0.2
        coef[2] = 0.066
        coef[3] = 0.0091
        coef[7] = 0.059
    else : # (D) Desfavor�vel
        coef[1] = 0.3
        coef[2] = 0.125
        coef[3] = 0.323
        coef[7] = 0.04

# Alterna em um array a sele��o de um conjunto de vari�veis para definir o eixo Y do gr�fico a ser gerado
# Exemplo : YN = [[x(1), y(1), z(1)] , [x(2), y(2), z(2)], [x(n), y(n), z(n)]] & TN = [1, 2, 3, 4, ...]
# indicesYN = array de Boolean com 1 nas equa��es que desejamos usar
def filtrar_variavel (YN, indicesYN):
    filtro = []
    for i in range(0, len(YN)): # Para cada yn que foi adicionado em YN. Ou seja, Y0, Y1, Y2, ..., YN
        soma = 0
        for j in range(0, len(YN[0])): # Itera sobre as vari�veis de YN. Ou seja, x, y, z do exemplo acima
            if (indicesYN[j] == 1):
                soma += YN[i][j]
        filtro.append(soma)

    return filtro

# Fun��o respons�vel pela indica��o dos eixos que ser�o desenhados no gr�fico
def eixos (matriz, vetor):
    resp = []
    for i in range(0, len(vetor)):
        resp.append([])
    for linha in matriz:
        for i in range(0, len(linha)):
            if vetor[i]:
                resp[i].append(linha[i])
    resp2 = []
    for item in resp:
        if item != []:
            resp2.append(item)
    return resp2

# Fun��o respons�vel efetivamente pela gera��o do gr�fico
def desenha_grafico (titulo, eixoX, eixo, nome_eixoX, nome_eixoY, nome_das_curvas):
    grafico = plt.figure()
    plt.title(titulo)
    if type (eixo) is list: # Se for um conjunto de valores a serem plotados...
        for item in eixo: # (x, y[N])
            plt.plot(eixoX,item , label = nome_das_curvas.pop(0))
    else: # Se for somente um valor (x, y)...
        plt.plot(eixoX,eixo)

    plt.ylabel(nome_eixoY)
    plt.xlabel(nome_eixoX)
    #plt.show()
    return grafico

# Realiza��o de um passo (k) do m�todo Runge-Kutta
def kutta(yk, h, f):
    v1 = escalarXvetor(h, f)
    return somaVetor(yk, v1)

# Varia��o do valor das equa��es do modelo matem�tico ao longo do tempo
def f(t, y):

    global Cfixo
    global coef

    ano_anterior = int(int(t) / 360) * 360 # Quando mudar de ano, retorna os per�odos 'F', 'I' e 'D'

    if(t > 120 + ano_anterior and t <= 240 + ano_anterior and Cfixo != 300):
        Cfixo = 300
        atualiza_coeficientes()
    elif ( t > 240 + ano_anterior and t <= 360 + ano_anterior and Cfixo != 500):
        Cfixo = 500
        atualiza_coeficientes()
    elif( t <= 120 + ano_anterior and Cfixo != 700):
        Cfixo = 700
        atualiza_coeficientes()

    ## Equa��es de Varia��o da Popula��o de Mosquitos ##
    f1 = coef[0] * ((1.0 - (y[0] / Clinha)) * (y[3]+y[4]+y[5]))  - ((coef[1] + coef[4]) * y[0]) # P�gina 44, Equa��o 'E(t)'
    f2 = (coef[1] * y[0]) - ((coef[2] + coef[5] + coef[10]) * y[1]) # P�gina 44, Equa��o 'L(t)'
    f3 = (coef[2] * y[1])  - ((coef[3] + coef[6] + coef[11]) * y[2]) # P�gina 44, Equa��o 'P(t)'
    f4 = (coef[3] * y[2]) - (((coef[13] * (0/N)) + coef[7] + coef[12]) * y[3]) # P�gina 44, Equa��o 'W1(t)'
    f5 = (coef[13] * (N*0.5/N) * y[3])  - ((coef[15] + coef[7] + coef[12]) * y[4]) # P�gina 44, Equa��o 'W2(t)'
    f6 = (coef[15] * y[4])  - ((coef[7] + coef[12]) * y[5]) # P�gina 44, Equa��o 'W3(t)'

    ## Equa��es de Varia��o da Popula��o de Seres Humanos ##
    #f7 = coef[19] * N - (coef[14] * (y[5]  / y[6] ) + coef[18]) * y[7] # P�gina 45, Equa��o 's(t)'
    #f8 = coef[14] * (y[5]  / y[6] ) * y[7]  - (coef[16] + coef[18]) * y[0] # P�gina 45, Equa��o 'e(t)'
    #f9 = coef[16] * y[0]  - (coef[17] + coef[18]) * y[8] # P�gina 45, Equa��o 'i(t)'
    #f10 = coef[17] * y[8]  - coef[18] * y[9] # P�gina 45, Equa��o 'r(t)'

    yFa = [f1,f2, f3, f4, f5, f6]

    return yFa

# Fun��o respons�vel pelo c�lculo do valor de Y1 que ser� utilizado no m�todo Runge-Kutta Expl�cito
def runge_kutta(y, h, t):
    #write_file(y)
    YN.append(y)
    TN.append(t)
    a = f(t, y)
    b = kutta(y, h/2, a)
    c = t + h/2
    d = f(c, b)
    y1 = kutta(y, h, d)
    #write_file(y1)
    return y1

# Fun��o criada para realizar os testes de converg�ncia somente com o Runge-Kutta de 2� Ordem
def runge_kutta_segunda_ordem_iterativo(y, h, t, iteracoes):
    for i in range(0, iteracoes):
        YN.append(y)
        TN.append(t)
        a = f(t, y)
        b = kutta(y, h/2, a)
        c = t + h/2
        d = f(c, b)
        y1 = kutta(y, h, d)
        y = y1
        t = t + h

# Fun��o criada para realizar os c�lculos do m�todo Runge-Kutta Expl�cito (YK atual, FK atual, H, Y anterior, F anterior)
def runge_kutta_explicito_iterativo(yk, fk, h, y0, f0, t, iteracoes):

    global YN

    for i in range(0, iteracoes):
        y1 = escalarXvetor(3, fk)
        y2 = subvetor(y1, f0)
        y3 = escalarXvetor(h/2, y2)
        yn = somaVetor(yk, y3)
        #print("Y"+ str(i) + ":")
        #print(yn)
        #print("t = "+str(t))
        #write_file(yn)
        YN.append(yn)
        TN.append(t)
        t = t + h
        fk = f(t, yn)
        y0 = yk
        f0 = f(t, yk)
        yk = yn

##############################
######## Programa ############
##############################

## Condi��es Iniciais ##

# Array de par�metros (taxas di�rias) extra�dos da tabela 1 da p�gina 46:
#      [ 0     1     2     3      4     5      6      7      8     9     10  11    12   13    14    15    16   17      18         19  ]
coef = [1.0, 0.33, 0.14, 0.346, 0.05, 0.05, 0.0167, 0.042, 0.04, 0.059, 0.0, 0.0, 0.0, 0.75, 0.375, 0.2, 0.1, 0.143, 0.000042, 0.00042]

dias = 7200.0 # Quantidade de dias para analisar

h = 0.01 # Valor da discretiza��o

iteracoes = int(dias / h) # Quantidade de itera��es do m�todo

t = 0 # Varia��o de Tempo

Et = 0.0 # Popula��o de Ovos
Lt = 0.0 # Popula��o de Larvas
Pt = 0.0 # Popula��o de Pupas
W1t = 2.0 # Popula��o de Mosquito Adulto Suscet�vel
W2t = 50.0 # Popula��o de Mosquito Adulto Exposto
W3t = 17.0 # Popula��o de Mosquito Adulto Infectado

Y0 = [float(Et), float(Lt), float(Pt), float(W1t), float(W2t), float(W3t)] #Y0

N = 500000.0 # Popula��o de Seres Humanos

Cfixo = 700.0 # Valor Referente ao Per�odo Favor�vel

Clinha = 1
Clinha = Clinha * Cfixo # Capacidade de Suporte Ambiental

atualiza_coeficientes()

YN = [] # Array de Varia��o de y

TN = [] # Array de Varia��o de t

#remove_file()

# Obtendo o valor de Y1 para utilizar no m�todo Runge-Kutta Expl�cito
Y1 = runge_kutta(Y0, h, t)

print("Y0: ", Y0)
print("Y1: ", Y1)

# Para realizar os testes de converg�ncia somente com o Runge-Kutta de 2� Ordem...
runge_kutta_segunda_ordem_iterativo(Y0, h, t, iteracoes)

# M�todo Expl�cito Iterativo
runge_kutta_explicito_iterativo(Y1, f(t, Y1), h, Y0, f(t, Y0), t + h, iteracoes)

## Gr�fico ##

filtro = [1, 1, 1, 1, 1, 1] # Selecionar W1, W2, W3
eixoY = filtrar_variavel(YN, filtro) # W(t)
titulo = ('Popula��o de Mosquitos X Dias')
nome_eixoY = ('Popula��o de Mosquitos')
nome_eixoX = ('Dias')
nome_das_curvas = ['Ovo', 'Larva', 'Pupa', 'Mosquito Adulto Suscet�vel(W1)', 'Mosquito Adulto Exposto(W2)', 'Mosquito Adulto Infectado(W3)']
eixo = eixos(YN, filtro)
graf = desenha_grafico (titulo, TN, eixo, nome_eixoX, nome_eixoY, nome_das_curvas)
plt.legend()
plt.show()
#!/usr/bin/python
# -*- coding: latin-1 -*-

import matplotlib.pyplot as plt
import os

##############################
########## Funções ###########
##############################

# Função responsável em deletar o arquivo 'valores.csv'
def remove_file():
    os.remove("valores.csv")

# Função responsável em criar o arquivo 'valores.csv'
def write_file(a):
    f = open("valores.csv", "a")
    for i in range (0, len(a) - 1):
        f.write(str(a[i]) + ';')
    f.write(str(a[len(a) - 1]) + '\n')
    f.close()

# Multiplicação de um vetor por um escalar
def escalarXvetor(e, v):
    for i in range (0, len(v)):
        v[i] = e * v[i]
    return v

# Adição de valores entre dois vetores
def somaVetor(v1, v2):
    resp = []
    for i in range(0, len(v1)):
        resp.append(v1[i] + v2[i])
    return resp

# Subtração de valores entre dois vetores
def subvetor(v1, v2):
    resp = []
    for i in range (0, len(v1)):
        resp.append(v1[i] - v2[i])
    return resp

# Função que atualiza os coeficientes:
# 'Taxa de Desenvolvimento de um Ovo para uma Larva',
# 'Taxa de Desenvolvimento de uma Larva para uma Pupa',
# 'Taxa de Desenvolvimento de uma Pupa para um Alado',
# 'Taxa de Mortalidade de Mosquito Alado' e
# 'Capacidade de Suporte Ambiental'
#  de acordo com a época do ano.
def atualiza_coeficientes():
    global Cfixo
    global coef
    if (Cfixo == 700): # (F) Favorável
        coef[1] = 0.33
        coef[2] = 0.14
        coef[3] = 0.346
        coef[7] = 0.042
    elif (Cfixo == 500): # (I) Intermediário
        coef[1] = 0.2
        coef[2] = 0.066
        coef[3] = 0.0091
        coef[7] = 0.059
    else : # (D) Desfavorável
        coef[1] = 0.3
        coef[2] = 0.125
        coef[3] = 0.323
        coef[7] = 0.04

# Alterna em um array a seleção de um conjunto de variáveis para definir o eixo Y do gráfico a ser gerado
# Exemplo : YN = [[x(1), y(1), z(1)] , [x(2), y(2), z(2)], [x(n), y(n), z(n)]] & TN = [1, 2, 3, 4, ...]
# indicesYN = array de Boolean com 1 nas equações que desejamos usar
def filtrar_variavel (YN, indicesYN):
    filtro = []
    for i in range(0, len(YN)): # Para cada yn que foi adicionado em YN. Ou seja, Y0, Y1, Y2, ..., YN
        soma = 0
        for j in range(0, len(YN[0])): # Itera sobre as variáveis de YN. Ou seja, x, y, z do exemplo acima
            if (indicesYN[j] == 1):
                soma += YN[i][j]
        filtro.append(soma)

    return filtro

# Função responsável pela indicação dos eixos que serão desenhados no gráfico
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

# Função responsável efetivamente pela geração do gráfico
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

# Realização de um passo (k) do método Runge-Kutta
def kutta(yk, h, f):
    v1 = escalarXvetor(h, f)
    return somaVetor(yk, v1)

# Variação do valor das equações do modelo matemático ao longo do tempo
def f(t, y):

    global Cfixo
    global coef

    ano_anterior = int(int(t) / 360) * 360 # Quando mudar de ano, retorna os períodos 'F', 'I' e 'D'

    if(t > 120 + ano_anterior and t <= 240 + ano_anterior and Cfixo != 300):
        Cfixo = 300
        atualiza_coeficientes()
    elif ( t > 240 + ano_anterior and t <= 360 + ano_anterior and Cfixo != 500):
        Cfixo = 500
        atualiza_coeficientes()
    elif( t <= 120 + ano_anterior and Cfixo != 700):
        Cfixo = 700
        atualiza_coeficientes()

    ## Equações de Variação da População de Mosquitos ##
    f1 = coef[0] * ((1.0 - (y[0] / Clinha)) * (y[3]+y[4]+y[5]))  - ((coef[1] + coef[4]) * y[0]) # Página 44, Equação 'E(t)'
    f2 = (coef[1] * y[0]) - ((coef[2] + coef[5] + coef[10]) * y[1]) # Página 44, Equação 'L(t)'
    f3 = (coef[2] * y[1])  - ((coef[3] + coef[6] + coef[11]) * y[2]) # Página 44, Equação 'P(t)'
    f4 = (coef[3] * y[2]) - (((coef[13] * (0/N)) + coef[7] + coef[12]) * y[3]) # Página 44, Equação 'W1(t)'
    f5 = (coef[13] * (N*0.5/N) * y[3])  - ((coef[15] + coef[7] + coef[12]) * y[4]) # Página 44, Equação 'W2(t)'
    f6 = (coef[15] * y[4])  - ((coef[7] + coef[12]) * y[5]) # Página 44, Equação 'W3(t)'

    ## Equações de Variação da População de Seres Humanos ##
    #f7 = coef[19] * N - (coef[14] * (y[5]  / y[6] ) + coef[18]) * y[7] # Página 45, Equação 's(t)'
    #f8 = coef[14] * (y[5]  / y[6] ) * y[7]  - (coef[16] + coef[18]) * y[0] # Página 45, Equação 'e(t)'
    #f9 = coef[16] * y[0]  - (coef[17] + coef[18]) * y[8] # Página 45, Equação 'i(t)'
    #f10 = coef[17] * y[8]  - coef[18] * y[9] # Página 45, Equação 'r(t)'

    yFa = [f1,f2, f3, f4, f5, f6]

    return yFa

# Função responsável pelo cálculo do valor de Y1 que será utilizado no método Runge-Kutta Explícito
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

# Função criada para realizar os testes de convergência somente com o Runge-Kutta de 2ª Ordem
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

# Função criada para realizar os cálculos do método Runge-Kutta Explícito (YK atual, FK atual, H, Y anterior, F anterior)
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

## Condições Iniciais ##

# Array de parâmetros (taxas diárias) extraídos da tabela 1 da página 46:
#      [ 0     1     2     3      4     5      6      7      8     9     10  11    12   13    14    15    16   17      18         19  ]
coef = [1.0, 0.33, 0.14, 0.346, 0.05, 0.05, 0.0167, 0.042, 0.04, 0.059, 0.0, 0.0, 0.0, 0.75, 0.375, 0.2, 0.1, 0.143, 0.000042, 0.00042]

dias = 7200.0 # Quantidade de dias para analisar

h = 0.01 # Valor da discretização

iteracoes = int(dias / h) # Quantidade de iterações do método

t = 0 # Variação de Tempo

Et = 0.0 # População de Ovos
Lt = 0.0 # População de Larvas
Pt = 0.0 # População de Pupas
W1t = 2.0 # População de Mosquito Adulto Suscetível
W2t = 50.0 # População de Mosquito Adulto Exposto
W3t = 17.0 # População de Mosquito Adulto Infectado

Y0 = [float(Et), float(Lt), float(Pt), float(W1t), float(W2t), float(W3t)] #Y0

N = 500000.0 # População de Seres Humanos

Cfixo = 700.0 # Valor Referente ao Período Favorável

Clinha = 1
Clinha = Clinha * Cfixo # Capacidade de Suporte Ambiental

atualiza_coeficientes()

YN = [] # Array de Variação de y

TN = [] # Array de Variação de t

#remove_file()

# Obtendo o valor de Y1 para utilizar no método Runge-Kutta Explícito
Y1 = runge_kutta(Y0, h, t)

print("Y0: ", Y0)
print("Y1: ", Y1)

# Para realizar os testes de convergência somente com o Runge-Kutta de 2ª Ordem...
runge_kutta_segunda_ordem_iterativo(Y0, h, t, iteracoes)

# Método Explícito Iterativo
runge_kutta_explicito_iterativo(Y1, f(t, Y1), h, Y0, f(t, Y0), t + h, iteracoes)

## Gráfico ##

filtro = [1, 1, 1, 1, 1, 1] # Selecionar W1, W2, W3
eixoY = filtrar_variavel(YN, filtro) # W(t)
titulo = ('População de Mosquitos X Dias')
nome_eixoY = ('População de Mosquitos')
nome_eixoX = ('Dias')
nome_das_curvas = ['Ovo', 'Larva', 'Pupa', 'Mosquito Adulto Suscetível(W1)', 'Mosquito Adulto Exposto(W2)', 'Mosquito Adulto Infectado(W3)']
eixo = eixos(YN, filtro)
graf = desenha_grafico (titulo, TN, eixo, nome_eixoX, nome_eixoY, nome_das_curvas)
plt.legend()
plt.show()
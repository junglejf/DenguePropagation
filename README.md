# DenguePropagation
Analise de propagação da doença Dengue através do método de Runge-Kuta auxiliado por um método explícito

Neste trabalho abordamos apenas as equações relativas a população de mosquitos. 
<p align="center">
<img src="./Equacoes.png">
</p>

As variáveis de inicialização são:
```
##############################
#Inicializacao das variaveis#
##############################

#Valores iniciais
dias = 7200 # por quantos dias deseja executar a simulação
h = 0.19    


iteracoes = int(dias/h )


t = 0 
x = (1 *h)/0.04

Essas são exatamente as equações do mosquito da figura acima
#### Mosquito ####
Et = 225.0
Lt = 15.0
Pt = 50.0
W1t = 5.0
W2t = 20.0
W3t = 100.0

# Wt = W1t + W2t + W3t

### Humanos ###
St = 2.0
et = 5.0
It = 30.0 
Rt = 4.0


#Y0 = [float(Et), float(Lt), float(Pt), float(W1t), float(W2t), float(W3t), float(St),float(et), float(It), float(Rt)]
Y0 = [float(Et), float(Lt), float(Pt), float(W1t), float(W2t), float(W3t)]


Cfixo = 700.0     #Valor referente ao periodo favoravel   || Cfixo = 500 -> Intermediário || Cfico = 300 -> desfavorável
Ci = 0.5       #Valor do teorema do chute
Clinha = Ci * Cfixo     #capacidade de suporte ambiental
 ARRAY DE PARÂMETROS COM OS VALORES EXTRAÍDOS DA TABELA 1 coeficientes DA PÁGINA 46:
#        0     1     2     3      4     5      6      7      8     9     10  11    12   13    14    15    16   17      18         19
coef = [1.0, 0.33, 0.14, 0.346, 0.05, 0.05, 0.0167, 0.042, 0.04, 0.059, 0.0, 0.0, 0.0, 0.75, 0.375, 0.2, 0.1, 0.143, 0.000042, 0.00042]
```

Após a seleção dos parâmetros o passo seguinte é a execução do método implícito runge-kutta 1 vez para podermos executar o método explícito de passos múltiplo 2.

```
Y1 = range_kutta(Y0, h, t)
```
No método explícito utilizaremos com parâmetro Y1 calculado anteriormente e a solução Inicial Y0.
```
# Método explícito iterativo!
iterkutta = kutta_exp_iter(Y1, f(t, Y1), h, Y0, f(t, Y0), t+h, iteracoes)
```
A função f (ou vetor f) são as equações usadas no problema(nesse caso as 6 equações do mosquito) que está sendo aplicada nas soluções Y1 e Y0 inicialmente até YN e YN-1.
```
def f(t, y):
# Y0 = [float(Et), float(Lt), float(Pt), float(W1t), float(W2t), float(W3t), float(St),float(et) , float(It), float(Rt)]
#           y[0] ,    y[1]  ,  y[2]    ,  y[3]     ,    y[4]   , y[5]      ,  y[6]    ,   y[7]   ,  y[8]    ,  y[9]                
    global Cfixo
    global coef
    ano_anterior = int(int(t)/360)*360 # quando mudar de ano retorna os períodos F,I,D
    #Condições dinâmica do problema no qual o Ci varia ao longo do ano
    if(t > 120 + ano_anterior and t <= 240 + ano_anterior and Cfixo != 300):
        Cfixo = 300
        atualiza_coeficientes()
    elif ( t > 240 + ano_anterior and t <= 360 + ano_anterior and Cfixo != 500):
        Cfixo = 500
        atualiza_coeficientes()
    elif( t <= 120 + ano_anterior and Cfixo != 700):
        Cfixo = 700
        atualiza_coeficientes()

    ## Mosquito ## 
    f1 = pn ( ((coef[0] * ((1.0 - (y[0] / Clinha)))) ) * (y[3]+y[4]+y[5])  - (coef[1] + (coef[4] * y[0]))  )     # Página 44, equao E(t)
    f2 = pn((coef[1] * y[0]) - ((coef[2] + coef[5] + coef[10]) * y[1])       )  # Página 44, equação L(t)
    f3 = pn((coef[2] * y[1])  - ((coef[3] + coef[6] + coef[11]) * y[2])       )  # Página 44, equação P(t)
    f4 = pn((coef[3] * y[2]) - (((coef[13] * (0/N)) + coef[7] + coef[12]) * y[3]) )        # Página 44, equação W1(t)
    f5 = pn((coef[13] * (0/N) * y[3])  - ((coef[15] + coef[7] + coef[12]) * y[4]) )        # Página 44, equação W2(t)
    f6 = pn((coef[15] * y[4])  - ((coef[7] + coef[12]) * y[5])    )     # Página 44, equação W3(t)

    yFa = [f1,f2, f3, f4, f5, f6]         
    return yFa
```

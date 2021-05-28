"""
X^2 - 3X - 4

X = 1
x = 
"""
from random import randint, uniform
from math import  ceil
import numpy as np

# solução otima
def otima(ind):
    x = bin_to_dec(ind)
    y = x*x - 3*x - 4
    return y

# ROTINA DE ORDENAÇÃO
def sort(lista,fit,qt):

    for i in range(0,qt-1):
        for j in range(i+1,qt):
            if fit[i]<fit[j]:
                aux    = fit[i]
                fit[i] = fit[j]
                fit[j] = aux

                aux      = lista[i]
                lista[i] = lista[j]
                lista[j] = aux

    return lista, fit

# OPERADOR DE SELEÇÃO - TORNEIO
def torneio(f):
    i = randint(0,len(f)-1)
    j = randint(0,len(f)-1)

    if f[i]>f[j]:
        return i
    else:
        return j

# OPERADOR DE SELEÇÃO - ROLETA
def roleta(f):
    soma = 0
    j = 0
    ale = uniform(0,1)
    while soma<ale:
        soma += f[j]
        j += 1

    return j-1

# ROTINA PARA GERAR SOLUÇÃO INICIAL
def pop_inicial(tp):

    p = np.zeros((tp,8),dtype=int)

    # loop para gerar cada individuo
    for i in range(tp):
        # randomico uniforme
        for j in range(8):
            p[i][j] = randint(0,1)

    return p

# FIM DA ROTINA

def bin_to_dec(b):
    x = 0
    for j in range(1,n):
        x += b[j]*pow(2,7-j)
    if x==1:
        x = -x
    return x


def aptidao(pop,tp):

    f = np.zeros(tp,dtype=float)
    soma  = 0
    for i in range(tp):
        # converter para decimal
        x = bin_to_dec(pop[i])

        # aplicar na formula
        f[i] = abs(x*x - 3*x - 4)
        if f[i]==0:
            f[i] = 9999
        else:
            f[i] = 1/f[i]

        # soma para depois divirs
        soma += f[i]

    for i in range(tp):
        f[i] = f[i]/soma

    return f

# rotina cruzamento
def cruzamento(pop,fit,tp,tc):

    # quantidade de cruzamentos
    qc = ceil(tp*tc)

    # define estrutura para descendentes
    d = np.zeros((qc*2,n),dtype=int)
    k = 0

    # ponto de corte
    corte = randint(1,n-2)

    # executar os cruzamento para gerar descendentes
    for i in range(qc):

        # ===> seleciona  o primeiro pai - roleta
        p1 = roleta(fit)
        p2 = roleta(fit)

        # primeira parte do descendente
        for j in range(0,corte):
            d[k][j]   = pop[p1][j]
            d[k+1][j] = pop[p2][j]

        # segunda parte do descendente
        for j in range(corte,n):
            d[k][j]   = pop[p2][j]
            d[k+1][j] = pop[p1][j]
        k += 2

    return d

# rotina mutação
def mutacao(desc,tp,tm):

    # quantidade de cruzamentos
    qd = len(desc)

    # quantidade de mutação
    qm = ceil(tp*tm)

    d = np.zeros((qm+qd,n),dtype=int)

    for i in range(qd):
        d[i] = desc[i]

    k = qd

    # executar mutação por troca simples
    for i in range(qm):

        # seleciona  um descendente
        ind = randint(0,qd-1)
        aux = []
        aux = d[ind]

        # mutacao troca simples
        pos = randint(0,n-1)
        aux[pos] = 1 - aux[pos]
        d[k] = aux

        """
        # mutação translocação
        pos1 = randint(0,n-1)
        pos2 = randint(0,n-1)
        x = aux[pos1]
        aux[pos1] = aux[pos2]
        aux[pos2] = x
        d[k] = aux
        """
        k += 1

    return d

# ROTINA GERA NOVA POPULAÇÃO
def nova_pop(p,d,qp,qd,ig):
    npop = np.zeros((qp,n),dtype=int)
    elite = int(ig*qp)

    # nova popualçao a partir dos pais
    for i in range(0,elite):
        npop[i] = p[i]

    # nova população a partir dos filhos
    for i in range(elite,qp):
        npop[i] = d[i-elite]

    return npop

# ROTINA SUBIDA DE ENCOSTA
def ag(tp,tc,tm,ig,ng):

    # gera a pop INICIAL
    pop = pop_inicial(tp)
    fit = aptidao(pop,tp)
    pop, fit = sort(pop,fit,tp)
    si = pop[0]

    for t in range(ng):
        desc = cruzamento(pop,fit,tp,tc)
        desc = mutacao(desc,tp,tm)

        fit_d = aptidao(desc,len(desc))
        desc, fit_d = sort(desc,fit_d,len(desc))

        #print("\n",pop, fit)
        pop = nova_pop(pop,desc,tp,len(desc),ig)
        fit = aptidao(pop,tp)
        pop, fit = sort(pop,fit,tp)
        if otima(pop[0])==0:
            return si, pop[0], t

    return si, pop[0], t



# FIM DA ROTINA


# CÓDIGO PRINCIPAL
n = 8                   # tamanho do vetor
TP = [10,50,100,200]    # tamanho da população
TC = [0.5,0.6,0.8]      # taxa de cruzamento
TM = [0,0.05,0.1,0.2]   # taxa de mutação
IG = [0,0.1,0.2,0.5]    # intervalo de geração
NG = [10,50,100]        # número de gerações

for i1 in range(len(TP)):
    for i2 in range(len(TC)):
        for i3 in range(len(TM)):
            for i4 in range(len(IG)):
                for i5 in range(len(NG)):
                    si, s, t = ag(TP[i1],TC[i2],TM[i3],IG[i4],NG[i5])
                    print(TP[i1],TC[i2],TM[i3],IG[i4],
                          NG[i5],bin_to_dec(s),bin_to_dec(si),t)

# FIM CÓDIGO PRINCIPAL
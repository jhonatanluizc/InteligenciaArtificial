import csv
import random

# Rotina de ordenação
import numpy as np

def sort(pop, fit):
    qt = len(pop)
    for i in range(0, qt - 1):
        for j in range(i + 1, qt):
            if fit[i] < fit[j]:
                aux = fit[i]
                fit[i] = fit[j]
                fit[j] = aux

                aux = pop[i]
                pop[i] = pop[j]
                pop[j] = aux

    return pop, fit

#GERAR MATRIZ ALEATÓRIA
def geraPontos(n):
  ponto = []
  for i in range(n):
    linha = []
    for j in range(n):
      if i == j:
        linha.append(0)
      else:
        linha.append(random.randint(5, 20))
    ponto.append(linha)
  return ponto

#GERAR SOLUCAO INICIAL ALEATORIA
def solucao_inicial(s_pontos):
  s_inicial = []
  for x in range(len(s_pontos)):
    s_inicial.append(x)
    random.shuffle(s_inicial)
  return(s_inicial)

def gerar_populacao(tam_p, dim):
    # populacao = np.zeros((tam_p, dim), dtype = int)
    populacao = []
    for y in range(tam_p):
        cromossomo = []
        for x in range(dim):
            cromossomo.append(x)
        random.shuffle(cromossomo)
        # populacao[y] = cromossomo
        populacao.append(cromossomo)
    return populacao

def aptidao(matrix, pop):
    aptidoes = []
    soma = 0
    for cromo in pop:
        avalia = 0
        for x in range(len(cromo)):
            if x < (len(cromo) - 1):
                avalia = avalia + matrix[cromo[x]][cromo[x + 1]]
            else:
                avalia = avalia + matrix[cromo[x]][cromo[0]]
            soma += avalia
        aptidoes.append(avalia)

    for i in range(len(pop)):
        aptidoes[i] = aptidoes[i] / soma

    return aptidoes

def avalia(matrix, cromo):
    soma = 0

    avalia = 0
    for x in range(len(cromo)):
        if x < (len(cromo) - 1):
            avalia = avalia + matrix[cromo[x]][cromo[x + 1]]
        else:
            avalia = avalia + matrix[cromo[x]][cromo[0]]
        soma += avalia

    return soma

def cruzamento(sucessor1, sucessor2):

    corte = int((len(sucessor1) - 1) / 2)

    descendente1 = sucessor1[:corte]
    descendente2 = sucessor2[:corte]

    descendente11 = sucessor2[corte:]
    descendente22 = sucessor1[corte:]

    descendente_final1 = descendente1 + descendente11
    descendente_final2 = descendente2 + descendente22

    return [descendente_final1, descendente_final2]


def cruzamentos(pop, tc):
    tp = len(pop)
    qc = int(tc * tp)

    filhos = []

    for x in range(qc):
        aleatorio1 = random.randint(0, len(pop) - 1)
        aleatorio2 = random.randint(0, len(pop) - 1)
        filho = cruzamento(pop[aleatorio1], pop[aleatorio2])

        filhos += filho

    return filhos

def mutacao(desc, tp, tm):
    # quantidade de cruzamentos
    qd = len(desc)

    # quantidade de mutação
    qm = int(qd * tm)

    d = np.zeros((qm + qd, 8), dtype=int).tolist()

    for i in range(qd):
        d[i] = desc[i]

    k = qd

    # executar mutação por troca simples
    for i in range(qm):
        # seleciona um descendente
        ind = random.randint(0, qd - 1)
        aux = []
        aux = d[ind]

        # mutação translocação
        pos1 = random.randint(0, 8 - 1)
        pos2 = random.randint(0, 8 - 1)
        x = aux[pos1]
        aux[pos1] = aux[pos2]
        aux[pos2] = x
        d[k] = aux
        k += 1

    return d

# Gera uma nova população
def nova_pop(p, d, qp, qd, ig):
    npop = np.zeros((qp, 8), dtype=int).tolist()
    elite = int(ig * qp)

    # nova população a partir dos pais
    for i in range(0, elite):
        npop[i] = p[i]
    # nova população a partir dos filhos
    for i in range(elite, qp):
        npop[i] = d[i - elite]

    return npop

def ag(tp, tc, tm, ig, ng, n):
    matrix = geraPontos(n)

    # gera a pop INICIAL
    pop = gerar_populacao(tp, n)
    fit = aptidao(matrix, pop)
    pop, fit = sort(pop, fit)

    si = pop[0]

    for t in range(ng):
        desc = cruzamentos(pop, tc)
        desc = mutacao(desc, tp, tm)

        fit_d = aptidao(matrix, desc)
        desc, fit_d = sort(desc, fit_d)

        pop = nova_pop(pop, desc, tp, len(desc), ig)
        fit = aptidao(matrix, pop)
        pop, fit = sort(pop, fit)

    return si, pop[0], t, matrix


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
                    si, s, t, matriz = ag(TP[i1], TC[i2], TM[i3], IG[i4], NG[i5], n)
                    a_s = avalia(matriz, s)
                    a_si = avalia(matriz, si)
                    ganho = (a_si - a_s) * 100 / a_si
                    print(TP[i1], TC[i2], TM[i3], IG[i4], NG[i5], s, si, t, a_s, a_si, ganho)


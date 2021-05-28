import random
import numpy as np
import math

matriz_B = []
qtd_B = 0


# Geração de matriz aleatória:
def gera_Matriz(n):
    for l in range(n):
        linha = []
        for c in range(n):
            if (l == c):
                linha.append(0)
            else:
                linha.append(random.randint(5, 15))
        matriz_B.append(linha)


def solucao_ini(n):
    global qtd_B
    global matriz_B
    qtd_B = n
    # Gerando Solução inicial aleatória
    solution_Ini = []
    while (len(solution_Ini) != qtd_B):
        aleatorio = random.randint(1, qtd_B)
        # Verifica se o número gerado já existe no vetor
        if ((aleatorio in solution_Ini) == False):
            solution_Ini.append(aleatorio)
    return solution_Ini


def populacao_Ini(tp, n):
    populacao = np.zeros((tp, n), dtype=int).tolist()
    for i in range(tp):
        populacao[i] = solucao_ini(n)
    return populacao


# Contabiliza os custos
def avalia(s):
    n = []
    soma = 0
    # Ajusta o range
    for b in s:
        n.append(b - 1)

    # contabiliza a soma
    for i in n:
        # verifica se é diferente do ultimo item do vetor
        if (n.index(i) != (qtd_B - 1)):
            # verifica se possui o valor máximo do range
            if (i == (qtd_B - 1)):
                prox = n.index(i) + 1
                soma += matriz_B[i][n[prox]]
            else:
                soma += matriz_B[i][n[n.index(i) + 1]]
        else:
            soma += matriz_B[i][n[0]]
    return soma


def aptidao(pop, tp):
    soma = 0
    f = []
    for i in range(tp):
        f.append(1 / avalia(pop[i]))
        soma += f[i]
    for i in range(tp):
        f[i] = f[i] / soma
    return f


def roleta(fit):
    i = 0
    soma = 0
    r = random.uniform(0, 1)
    while (soma < r):
        soma += fit[i]
        i += 1
    return i - 1


def cross(pop, fit, tp, tc):
    # quantidade de cruzamentos
    qc = math.ceil(tp * tc)

    # define a estrutura para os descendentes
    d = np.zeros((qc * 2, qtd_B), dtype=int).tolist()
    k = 0

    # define o ponto de corte
    ptCorte = 0
    while (ptCorte == 0 or ptCorte == qtd_B - 1):
        ptCorte = random.randint(1, qtd_B - 1)

    # executa o cruzamento
    for i in range(qc):
        p1 = roleta(fit)
        p2 = roleta(fit)
        # primeira parte do descendente
        for j in range(0, ptCorte):
            d[k][j] = pop[p1][j]
            d[k + 1][j] = pop[p2][j]

        # segunda parte do descendente
        for j in range(ptCorte, qtd_B):
            d[k][j] = pop[p2][j]
            d[k + 1][j] = pop[p1][j]
        k += 2

    for i in range(2 * qc):
        aux = list(range(1, qtd_B + 1))
        random.shuffle(aux)

        for j in range(0, ptCorte):
            aux.remove(d[i][j])
        j = ptCorte
        while (len(aux) > 0):
            if (d[i].count(aux[0]) == 0):
                if (d[i].count(d[i][j]) > 1):
                    d[i][j] = aux[0]
                    del aux[0]
                    j += 1
                else:
                    j += 1
            else:
                del aux[0]
    return d


def mutacao(desc, tp, tm):
    # quantidade de cruzamentos
    qd = len(desc)

    # quantidade de mutação
    qm = math.ceil(tp * tm)

    d = np.zeros((qm + qd, qtd_B), dtype=int).tolist()

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
        pos1 = random.randint(0, qtd_B - 1)
        pos2 = random.randint(0, qtd_B - 1)
        x = aux[pos1]
        aux[pos1] = aux[pos2]
        aux[pos2] = x
        d[k] = aux
        k += 1

    return d


# Gera uma nova população
def new_pop(p, d, qp, qd, ig):
    npop = np.zeros((qp, qtd_B), dtype=int).tolist()
    elite = int(ig * qp)

    # nova população a partir dos pais
    for i in range(0, elite):
        npop[i] = p[i]
    # nova população a partir dos filhos
    for i in range(elite, qp):
        npop[i] = d[i - elite]

    return npop


# Rotina de ordenação
def sort(pop, fit, qt):
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


# Rotina de Subida de Encosta
def ag(tp, tc, tm, ig, ng, bairros):
    # gera a pop inicial
    pop = populacao_Ini(tp, bairros)
    fit = aptidao(pop, tp)
    pop, fit = sort(pop, fit, tp)

    si = pop[0]

    for t in range(ng):
        desc = cross(pop, fit, tp, tc)
        desc = mutacao(desc, tp, tm)

        fit_d = aptidao(desc, len(desc))
        desc, fit_d = sort(desc, fit_d, len(desc))

        pop = new_pop(pop, desc, tp, len(desc), ig)
        fit = aptidao(pop, tp)
        pop, fit = sort(pop, fit, tp)
    return si, pop[0], t


# Programa principal
print("matrix", gera_Matriz(6))
TP = [10, 50, 100, 200]  # tamanho da população
TC = [0.5, 0.6, 0.8]  # taxa de cruzamento
TM = [0, 0.05, 0.1, 0.2]  # taxa de mutação
IG = [0, 0.1, 0.2, 0.5]  # intervalo de geração
NG = [10, 50, 100]  # número de gerações

for i1 in range(len(TP)):
    for i2 in range(len(TC)):
        for i3 in range(len(TM)):
            for i4 in range(len(IG)):
                for i5 in range(len(NG)):
                    si, s, t = ag(TP[i1], TC[i2], TM[i3], IG[i4], NG[i5], 6)
                    print(TP[i1], TC[i2], TM[i3], IG[i4],
                          NG[i5], avalia(s), avalia(si), t)

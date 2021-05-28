import random
import math
import csv

# ARRAY COM OS NOMES DOS ITENS
nomes = ["garrafa com água", "celular", "canivete", "faca", "bússola", "tijolo", "biscoito", "bolacha", "repelente",
         "caneca de plástico", "kit de primeiros socorros", "caixa de fósforo", "protetor solar", "lanterna", "corda",
         "miojo cup noodles", "livro", "rádio", "barraca", "bateria"]

# ARRAY COM OS PESOS DOS ITENS
pesos = [0.51, 0.2, 0.075, 0.12, 0.2, 2.2, 0.2, 0.2, 0.1, 0.09, 1.5, 0.03, 0.1, 0.31, 0.4, 0.069, 0.3, 0.5, 2.3, 0.7]

# ARRAY DE VALOR (ATRIBUIDO PARA DIZER O QUANTO O ITEM SERIA RELEVANTE DE SE TER NA MOCHILA)
valores = [9, 8, 7, 5, 5, 0, 9, 8, 6, 4, 9, 6, 3, 7, 3, 8, 2, 3, 10, 1]

# ARRAY COM TODAS AS INFORMACOES DOS ITENS
itens = [nomes, pesos, valores]

# LIMITE DE PESO QUE PODE SER CARREGADO NA MOCHILA
limite = 7

# ROTINA PARA GERAR UMA SOLUÇÃO
def solucaoAleatoria(array_itens):
    solucao = []
    pesoAtual = 0
    while pesoAtual <= limite:
        aleatorio = random.randint(0, len(array_itens[0]) - 1)
        if (aleatorio not in solucao):
            solucao.append(aleatorio)
            pesoAtual += pesos[aleatorio]
    if pesoAtual > limite:
        solucao.pop(-1)
    return solucao

# ROTINA PARA GERAR SOLUÇÃO INICIAL
def gerar_cromossomos(array_itens, max):
    cromossomos = []
    solucoes = []

    # CRIA SOLUCOES ALEATORIAS
    while (True):
        solucao = solucaoAleatoria(array_itens)
        if solucao not in solucoes: solucoes.append(sorted(solucao))
        if len(solucoes) == max: break

    for solucao in solucoes:
        cromossomo = []

        #SE O INDICE EXISTIR NA SOLUCAO O VALOR ATRIBUIDO FICA COMO 1
        for indiceArray in range(len(array_itens[0])):
            if indiceArray in solucao:
                cromossomo.append(1)
            else:
                cromossomo.append(0)

        cromossomos.append(cromossomo)

    return cromossomos

# ROTINA PARA GERAR UMA APTIDAO
def aptidao(array_itens, cromossomo):
    nota = 0
    for x in range(len(cromossomo)):
        if (cromossomo[x] == 1):
            nota = nota + array_itens[2][x]
    return int(nota)

# ROTINA PARA GERAR TODAS AS APTDOES DA POPULACAO
def gerar_aptidoes(array_itens, array_cromossomos):
    notas = []

    for cromossomo in array_cromossomos:
        notas.append(aptidao(array_itens, cromossomo))

    aptidoes = []
    for nota in notas:
        aptidoes.append(nota / (sum(notas)))

    return aptidoes

# ROTINA PARA MEDIR O PESO
def medir_peso(array_itens, cromossomo):
    peso = 0
    for x in range(len(cromossomo)):
        if (cromossomo[x] == 1):
            peso = peso + array_itens[1][x]
    return peso

# ROTINA DE CRUZAMENTO
def cruzamento(pai, mae):
    corte = random.randint(0, len(pai) - 1)

    filho1 = pai[0:corte] + mae[corte: len(pai)]
    filho2 = mae[0:corte] + pai[corte: len(mae)]

    return [filho1, filho2]

# ROTINA PARA GERAR DECENDENTES
def gerar_descendentes(cromossomos, operador_filhos):
    quantidade_filhos = int(len(cromossomos) * operador_filhos)
    descendentes = []

    for x in range(quantidade_filhos):
        mae = random.randint(0, len(cromossomos) - 1)
        pai = random.randint(0, len(cromossomos) - 1)

        filhos = cruzamento(cromossomos[pai], cromossomos[mae])
        descendentes += filhos

    return descendentes

# ROTINA DE MUTACAO
def mutacao(array_itens, mutacao_cromossomo, peso_max):
  cont = 0
  tentativa = 0

  while True:
    posicao_aleatoria = random.randint(0, len(mutacao_cromossomo) - 1)
    if mutacao_cromossomo[posicao_aleatoria] == 0:
      mutacao_cromossomo[posicao_aleatoria] = 1
      cont = cont + 1
    else:
      tentativa += 1
    if cont == 2 or tentativa > 3:
      break

  while True:
    peso = medir_peso(array_itens, mutacao_cromossomo)
    if peso <= peso_max:
      break
    else:
      posicao_aleatoria = random.randint(0, len(mutacao_cromossomo) - 1)
      if mutacao_cromossomo[posicao_aleatoria] == 1:
        mutacao_cromossomo[posicao_aleatoria] = 0

  return mutacao_cromossomo

# ROTINA PARA DERAR MUTACAO EM UMA POPULACAO
def gerar_mutacoes(array_itens, cromossomos, peso_max, operador_mutacao):
    quantidade_mutacao = int(len(cromossomos) * operador_mutacao)

    for x in range(quantidade_mutacao):
        aleatorio = random.randint(0, len(cromossomos) - 1)
        cromossomos[aleatorio] = mutacao(array_itens, cromossomos[aleatorio], peso_max)

    return cromossomos

# ROTINA DE ORDENAÇÃO
def sort(lista, fit):
    for i in range(len(lista)):
        for j in range(len(lista) - 1):
            if fit[i] > fit[j]:
                aux = fit[i]
                fit[i] = fit[j]
                fit[j] = aux

                aux = lista[i]
                lista[i] = lista[j]
                lista[j] = aux

    return lista, fit

# ROTINA PARA CRIAR UMA NOVA POPULACAO
def nova_pop(p,d,ig):
    qp = len(p)
    elite = int(ig * qp)

    npop = []

    # NOVA POPULACAO A PARTIR DOS PAIS
    for i in range(0, elite):
        npop.append(p[i])

    # NOVA POPULACAO A PARTIR DOS FILHOS
    for i in range(elite, qp):
        npop.append(d[i])

    # ADEQUAR OS CROMOSSOMOS AO PESO
    for i in range(len(npop)):
        cromossomo = npop[i]

        while True:
            if( medir_peso(itens, cromossomo) > limite):
                posAleatoria = random.randint(0, len(cromossomo) - 1)
                if(cromossomo[posAleatoria] == 1):
                    cromossomo[posAleatoria] = 0
            else:
                npop[i] = cromossomo
                break

    return npop

# ROTINA MOCHILA
def mochila(tp, tc, tm, ig, ng):

    # GERA A POPULACAO INICIAL
    pop = gerar_cromossomos(itens, tp)

    # CALCULA AS APTIDOES DA POPULACAO
    fit = gerar_aptidoes(itens, pop)

    # ORDENA A POPULACAO COM AS APTIDOES
    pop, fit = sort(pop, fit)

    si = pop[0]

    for t in range(ng):
        desc = gerar_descendentes(pop, tc)
        desc = gerar_mutacoes(itens, desc, limite, tm)

        fit_d = gerar_aptidoes(itens, desc)
        desc, fit_d = sort(desc, fit_d)

        pop = nova_pop(pop, desc, ig)
        fit = gerar_aptidoes(itens, pop)
        pop, fit = sort(pop, fit)

    return si, pop[0], t

# CALCULAR VALOR
def calcular_valor(cromossomo):
    valor = 0
    for x in range(len(cromossomo)):
        if cromossomo[x] == 1:
            valor += valores[x]
    return valor

#CALCULAR GANHO
def calcular_ganho(s, si):
    valor_s = calcular_valor(s)
    valor_si = calcular_valor(si)
    valor_t = (valor_s - valor_si) * 100 / valor_si
    valor_t = round(valor_t, 2)
    return valor_t

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
                    si, s, t = mochila(TP[i1], TC[i2], TM[i3], IG[i4], NG[i5])
                    print(TP[i1], TC[i2], TM[i3], IG[i4], NG[i5], s, si, t, calcular_ganho(s, si))

#caso queira salvar em csv
"""with open("data.csv", "w", newline='') as data:
    write = csv.writer(data)
    write.writerow(["TP", "TC", "TM", "IG", "NG", "S", "SI", "T", "GANHO"])
    for i1 in range(len(TP)):
        for i2 in range(len(TC)):
            for i3 in range(len(TM)):
                for i4 in range(len(IG)):
                    for i5 in range(len(NG)):
                        si, s, t = mochila(TP[i1], TC[i2], TM[i3], IG[i4], NG[i5])
                        print(TP[i1], TC[i2], TM[i3], IG[i4], NG[i5], s, si, t, calcular_ganho(s, si))
                        write.writerow([TP[i1], TC[i2], TM[i3], IG[i4], NG[i5], s, si, t, calcular_ganho(s, si)])
    data.close()"""



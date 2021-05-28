import random

# nomes dos itens
nomes = ["garrafa com água", "celular", "canivete", "faca", "bússola", "tijolo", "biscoito", "bolacha", "repelente", "caneca de plástico", "kit de primeiros socorros", "caixa de fósforo", "protetor solar", "lanterna", "corda", "miojo cup noodles", "livro", "rádio", "barraca", "bateria"]

# peso dos itens
pesos = [0.51, 0.2, 0.075, 0.12, 0.2, 2.2, 0.2, 0.2, 0.1, 0.09, 1.5, 0.03, 0.1, 0.31, 0.4, 0.069, 0.3, 0.5, 2.3, 0.7]

# valor atribuido ao item, o quanto esse item seria relevante para ser carregado na mochila
valores = [9, 8, 7, 5, 5, 0, 9, 8, 6, 4, 9, 6, 3, 7, 3, 8, 2, 3, 10, 1]

#array contendo as inforcaoes sobre os itens
itens = [nomes, pesos, valores]

# limite de peso que pode ser carregado na mochila
limite = 7

# tamanho da populacao inicial
tamP = 1000

# operador de decendentes em porcentagem .1 = 10%
opeD = .1

# operador de mutacao em porcentagem .1 = 10%
opeM = .2

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

def gerar_cromossomos(array_itens, max):
  cromossomos = []
  solucoes = []

  # criar solucoes aleatorias
  while (True):
      solucao = solucaoAleatoria(array_itens)
      if solucao not in solucoes: solucoes.append(sorted(solucao))
      if len(solucoes) == max: break
    
  for solucao in solucoes:
    cromossomo = []

    # se indice existir na solucao, o valor fica como 1
    for indiceArray in range(len(array_itens[0])):
      if indiceArray in solucao:
        cromossomo.append(1)
      else:
        cromossomo.append(0) 

    cromossomos.append(cromossomo)   
    
  return cromossomos

def aptidao(array_itens, cromossomo):
  nota = 0
  for x in range(len(cromossomo)):
    if(cromossomo[x] == 1):
      nota = nota + array_itens[2][x]
  return int(nota)

def gerar_aptidoes(array_itens, array_cromossomos):
  notas = []

  for cromossomo in array_cromossomos:
    notas.append(aptidao(array_itens, cromossomo))

  aptidoes = []
  for nota in notas:
    aptidoes.append(nota / (sum(notas)))

  return aptidoes

def medir_peso(array_itens, cromossomo):
  peso = 0
  for x in range(len(cromossomo)):
    if(cromossomo[x] == 1):
      peso = peso + array_itens[1][x]
  return peso

def cruzamento(pai, mae):

  corte = random.randint(0, len(pai) -1)

  filho1 = pai[0:corte] + mae[corte: len(pai)]
  filho2 = mae[0:corte] + pai[corte: len(mae)]

  return [filho1, filho2]

def gerar_descendentes(cromossomos, operador_filhos):

  quantidade_filhos = int(len(cromossomos) * operador_filhos)
  descendentes = []

  for x in range(quantidade_filhos):

    mae = random.randint(0, len(cromossomos) - 1)
    pai = random.randint(0, len(cromossomos) - 1)

    filhos = cruzamento(cromossomos[pai], cromossomos[mae])
    descendentes += filhos

  return descendentes


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

def gerar_mutacoes(array_itens, cromossomos, peso_max, operador_mutacao):

  quantidade_mutacao = int(len(cromossomos) * operador_mutacao)

  for x in range(quantidade_mutacao):

    aleatorio = random.randint(0, len(cromossomos) - 1)
    print("cromossomos")
    cromossomos[aleatorio] = mutacao(array_itens, cromossomos[aleatorio], peso_max)
    print("cromossomos2")

  return cromossomos

for x in range(100):
  cromossomos = gerar_cromossomos(itens, tamP)

  descendentes = gerar_descendentes(cromossomos, opeD)

  populacao = cromossomos + descendentes

  populacao = gerar_mutacoes(itens, populacao, limite, opeM)

  aptidoes = gerar_aptidoes(itens, populacao)

  print(x)



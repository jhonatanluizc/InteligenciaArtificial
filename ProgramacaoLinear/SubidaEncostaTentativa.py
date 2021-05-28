import random
nomes = ["garrafa com água", "celular", "canivete", "faca", "bússola", "tijolo", "biscoito", "bolacha", "repelente", "caneca de plástico", "kit de primeiros socorros", "caixa de fósforo", "protetor solar", "lanterna", "corda", "miojo cup noodles", "livro", "rádio", "barraca", "bateria"]
pesos = [0.51, 0.2, 0.075, 0.12, 0.2, 2.2, 0.2, 0.2, 0.1, 0.09, 1.5, 0.03, 0.1, 0.31, 0.4, 0.069, 0.3, 0.5, 2.3, 0.7]
valores = [9, 8, 7, 5, 5, 0, 9, 8, 6, 4, 9, 6, 3, 7, 3, 8, 2, 3, 10, 1]

itens = [nomes, pesos, valores]

limite = 7
solucao = []
pesoAtual = 0

def solucaoInicial(array_itens):
  #solucao inicial
  solucao = []
  pesoAtual = 0
  while pesoAtual <= limite:
    aleatorio = random.randint(0, len(array_itens[0]) - 1)
    if (aleatorio not in solucao):
      solucao.append(aleatorio)
      pesoAtual += pesos[aleatorio]
  #se peso passar do limite, remover ultimo item
  if pesoAtual > limite:
    solucao.pop(-1)
  return solucao

def avalia(array_itens, array_solucao):
  #avalia
  avalia = 0
  for x in array_solucao:
    avalia = avalia + array_itens[2][x]
  return avalia

def sucessor(array_itens, array_solucao, posicao):
  item_aleatorio = random.randint(0, len(array_itens[0]) - 1)
  array_solucao[posicao] = item_aleatorio
  
  peso_total = 0
  for x in array_solucao:
    peso_total = peso_total + array_itens[1][x]
  if peso_total > limite:
    array_solucao = sucessor(itens, array_solucao, posicao).copy()
  
  return array_solucao

def sucessores(array_itens, array_solucao, quantidade):
  array_sucessores = []
  posicao_aleatoria = random.randint(0, len(array_solucao) - 1)
  for x in range(quantidade):
    novo = sucessor(itens, array_solucao, posicao_aleatoria).copy()
    array_sucessores.append(novo)
  return array_sucessores

def melhor_sucessor(array_sucessores, array_itens, array_solucao):
  melhor = array_solucao.copy()
  melhor_avalia = avalia(array_itens, array_solucao.copy())
  for x in array_sucessores:
    if avalia(array_itens, x) > melhor_avalia:
      melhor = x
  return melhor


### Saidas
solucao_inicial = solucaoInicial(itens.copy())

solucao_atual = solucao_inicial
cont = 0
while True:
    
    avalia_atual = avalia(itens.copy(), solucao_atual.copy())
    print("{} = {}".format(solucao_inicial, avalia_atual))

    novos_sucessores = sucessores(itens.copy(), solucao_atual.copy(), 9)
    solucao_proxima = melhor_sucessor(novos_sucessores, itens, solucao_inicial)
    avalia_proxima = avalia(itens.copy(), solucao_proxima.copy())

    print("{} = {}".format(solucao_proxima, avalia_proxima))
    print()

    if(avalia_atual < avalia_proxima):
        solucao_atual = solucao_proxima
        cont = 0
    else:
      cont += 1
      if(cont == 3):
          print("{} = {}".format(solucao_atual, avalia_atual))         
          break

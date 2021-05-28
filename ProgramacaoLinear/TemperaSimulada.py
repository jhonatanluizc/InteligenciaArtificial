import random
from math import exp

nomes = ["garrafa com água", "celular", "canivete", "faca", "bússola", "tijolo", "biscoito", "bolacha", "repelente", "caneca de plástico", "kit de primeiros socorros", "caixa de fósforo", "protetor solar", "lanterna", "corda", "miojo cup noodles", "livro", "rádio", "barraca", "bateria"]

pesos = [0.51, 0.2, 0.075, 0.12, 0.2, 2.2, 0.2, 0.2, 0.1, 0.09, 1.5, 0.03, 0.1,     0.31, 0.4, 0.069, 0.3, 0.5, 2.3, 0.7]

valores = [9, 8, 7, 5, 5, 0, 9, 8, 6, 4, 9, 6, 3, 7, 3, 8, 2, 3, 10, 1]

itens = [nomes, pesos, valores]

#LIMITE DE PESO
limite = 7
solucao = []
pesoAtual = 0

#GERAR SOLUCAO INICIAL
#ADICIONAR ITENS NO ARRAY ATE CHEGAR NO PESO LIMITE, QUANDO CHEGAR NO LIMITE
#VERIFICAR SE NAO ESTÁ MAIOR, SE ESTIVER RETIRAR O ULTIMO ITEM
def solucaoInicial(array_itens):
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

#AVALIA
def avalia(array_itens, array_solucao):
  avalia = 0
  for x in array_solucao:
    avalia = avalia + array_itens[2][x]
  return avalia

#METODO PARA GERAR UM SUCESSOR
def sucessor(array_itens, array_solucao):
    nova_solucao = array_solucao.copy()
    posicao_aleatoria = random.randint(0, len(nova_solucao) - 1)
    item_aleatorio = random.randint(0, len(array_itens[0]) - 1)
    nova_solucao[posicao_aleatoria] = item_aleatorio
    return nova_solucao

#SO ENTRA NO ESP SE O VALOR FOR PIOR
#MÉTODO AUXILIAR(VA-VP)/TEMP
def auxiliar(a_vp, a_va, a_temp):
  return (exp(((-1*(a_vp-a_va))/a_temp)))
#GERAR ALEATORIO
def aleatorio():
  return random.randint(1, 999)/1000

#TEMPERATURA INICIAL
#TEMPERATURA FINAL
#PARAR QUANDO ATINGIR TEMPERATURA FINAL
temperatura_inicial = 200
temperatura_final = 50
temperatura_atual = 200
fator_redutor = 0.9

solucao_inicial = solucaoInicial(itens)
avalia_inicial = avalia(itens, solucao_inicial)

solucao_atual = solucao_inicial
avalia_atual = avalia(itens, solucao_atual)

while(True):
  solucao_proxima = sucessor(itens, solucao_atual)
  avalia_proxima = avalia(itens, solucao_proxima)
 
  if (avalia_proxima - avalia_atual) < 0:
    solucao_atual = solucao_proxima
    avalia_atual = avalia(itens, solucao_proxima)
  else:
    aux = auxiliar(avalia_proxima, avalia_atual, temperatura_atual)
    if(aleatorio() <= aux):
      solucao_atual = solucao_proxima
      avalia_atual = avalia(itens, solucao_proxima)
    temperatura_atual = temperatura_atual * fator_redutor
  if temperatura_atual < temperatura_final:
    break

solucao_proxima = sucessor(itens, solucao_atual)

print(solucao_inicial, avalia_inicial)
#print(solucao_atual, avalia_atual)
print(solucao_proxima, avalia_proxima)


#QUANDO O AUXILIAR É MAIOR DO QUE O ALEATORIO DESCE O SUCESSOR E A TEMPERATURA É MULTIPLICADA PELO FATOR REDUTOR
#CASO CONTRARIO MANTEM O ATUAL
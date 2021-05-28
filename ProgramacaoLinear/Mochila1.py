import random
nome = ["garrafa com água", "celular", "canivete", "faca", "bússola", "tijolo", "biscoito", "bolacha", "repelente", "caneca de plástico", "kit de primeiros socorros", "caixa de fósforo", "protetor solar", "lanterna", "corda", "miojo cup noodles", "livro", "rádio", "barraca", "bateria"]
peso = [0.51, 0.2, 0.075, 0.12, 0.2, 2.2, 0.2, 0.2, 0.1, 0.09, 1.5, 0.03, 0.1, 0.31, 0.4, 0.069, 0.3, 0.5, 2.3, 0.7]
valor = [9, 8, 7, 5, 5, 0, 9, 8, 6, 4, 9, 6, 3, 7, 3, 8, 2, 3, 10, 1]

#definicao do limite (peso maximo)
limite = 7

#correlacao
"""
for x in range(20):
  print("{} => {} {} {}".format(x, nome[x], peso[x], valor[x]))
"""

#solucao inicial
solucao = []
pesoAtual = 0
while pesoAtual <= limite:
  aleatorio = random.randint(0, len(nome) - 1)
  if (aleatorio not in solucao):
    solucao.append(aleatorio)
    pesoAtual += peso[aleatorio]

#se peso passar do limite, remover ultimo item
if pesoAtual > limite:
  solucao.pop(-1)

#avalia
avalia = 0
for x in solucao:
  avalia = avalia + valor[x]
print(avalia)

#sucessor
#pegar o atual, remover aleatoriamente 1 ou mais itens (algumas vezes) e retornar o melhor
sucessores = []
quantidade = 5

for x in range(quantidade):
  sucessores.append(solucao)
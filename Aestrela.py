import timeit
import random
import copy

META = [[1,2,3],[4,5,6],[7,8,0]]

#Estruturas de dadados que sao necessarios no processamento 
class Noh:
    def _init_(self,estado,nopai,g,h):
      self.estado = estado
      self.pai = nopai
      self.g = g
      self.h = h

      def _eq_(self,outro):
        return self.estado == outro.estado
        
      def __repr__(self):
        return str (self.estado)

      def getState(self):
        return self.estado

#Função que verifica se é possível solucionar o  puzzle:
def solucionavel(lista):
    inversoes = 0
    for i,e in enumerate(lista):
        if e == 0:
            continue
        for j in range(i+1, len(lista)):
            if lista[j]==0:
                continue
            if e > lista[j]:
                inversoes+=1
    if inversoes%2 == 1: #Se a possibilidade tiver inversoes impar, nao é solucionavel
        return False
    else:
        return True # Se for par, é solucionavel 

# Gera o tabuleiro inicial, de forma randomica!
def geraInicial(st=META[:]):
    lista= [j for i in st for j in i]
    while True:
        random.shuffle(lista)
        st = [lista[:3]]+[lista[3:6]]+[lista[6:]]
        if solucionavel(lista) and st!= META:  return st
    return 0

geraInicial()

# Localiza elemento qualquer no tabuleiro, no caso seria o "0"
def localizar(estado, elemento=0):
  for i in range(3):
    for j in range(3):
      if estado [i][j]==elemento:
        linha = i
        coluna = j
        return linha,coluna

# Dados o st1 e st2 calcula a distancia do quarterao do stado 1 ao estado 2 
def distanciaQuarteirao(st1,st2):
  dist = 0
  fora = 0
  for i in range(3):
    for j in range(3):
      if st1(i)(j)==0: continue
      i2, j2 = localizar(st2, st1[i][j])
      if i2 != i or j2 != j: fora += 1
      dist += abs(i2-1)+abs(j2-j)
  return dist + fora

#heuristica = distancia percorrida +  Distancia entre o estado atual e a meta 
def criarNo(estado,pai,g=0):
  h = g + distanciaQuarteirao(estado,META) # Função heuristica A*
  return Noh(estado,pai,g,h)

# o Nó sera interido na lista fronteira, que é a variavel de controle da busca
# A funcao insere o nó de uma maneira que se mantem ordenado des do estado inicial até o estado final
# ordena a fronteira pelo menor custo total
def inserirNoh(noh,fronteira):
  if noh in fronteira:
    return fronteira
  fronteira.append(noh)
  chave = fronteira[-1]
  j = len(fronteira)-2
  while fronteira[j].h > chave.h and j>=0:
    fronteira[j+1] = fronteira[j]
    fronteira[j] = chave
    j-=1
  return fronteira

# Movimentos do numero "0" ou o Branco 16:16
def moverAbaixo(estado):
  linha,coluna = localizar(estado)
  if linha < 2:
    estado[linha+1][coluna],estado[linha][coluna] = estado[linha][coluna],estado[linha+1][coluna]
  return estado

def moverAcima(estado):
  linha,coluna = localizar(estado)
  if linha > 0:
    estado[linha-1][coluna],estado[linha][coluna] = estado[linha][coluna],estado[linha-1][coluna]
  return estado

def moverDireita(estado):
  linha,coluna = localizar(estado)
  if linha < 2:
    estado[linha][coluna+1],estado[linha][coluna] = estado[linha][coluna],estado[linha][coluna+1]
  return estado

def moverEsquerda(estado):
  linha,coluna = localizar(estado)
  if linha > 0:
    estado[linha][coluna-1],estado[linha][coluna] = estado[linha][coluna],estado[linha][coluna-1]
  return estado

# Retorna todos os sucessores do nó
# Pega o nó que esta e calcula todos os estados alcansados apartir deste no (os nós antecessores), coloca em uma lista e retorna a lista de sucessores
def succ(noh):
  estado =noh.estado
  pai = noh.pai
  if pai:
    estadoPai = pai.estado
  else:
    estadoPai = None
  listaS = []
  l1 = moverAcima(copy.deepcopy(estado))
  if l1 != estado:
    listaS.append(l1)

  l2 = moverDireita(copy.deepcopy(estado))
  if l2 != estado:
    listaS.append(l2)

  l3 = moverAbaixo(copy.deepcopy(estado))
  if l3 != estado:
    listaS.append(l3)

  l4 = moverEsquerda(copy.deepcopy(estado))
  if l4 != estado:
    listaS.append(l4)
  
  return listaS

# Função de busca A*
# Realiza a busca do nó meta
def busca(max,nohInicio):
  print(nohInicio, ":")
  nmov = 0
  borda = [nohInicio]
  while borda:
    noh = borda.pop(0)
    if noh.estado == META:
      sol =[]
      while True: # Laco a mais para retornar apos ele encontrar o nó meta
        sol.append(noh.estado)
        noh =noh.pai
        if not noh: break
      sol.reverse()
      return sol,nmov
    nmov+=1
    if (nmov%(max/10))==0: print(nmov,end="....")
    if nmov>max: break
    sucs = succ(noh)
    for s in sucs:
      inserirNoh(criarNo(s,noh,noh.g+1),borda)
  return 0,nmov

# Recebendo a qualidade de vezes que ele vai rodar e apos isso ele vai rodar para cada umas das amostras, calculado o tempo e imprimindo um relatorio dos resultados em quanto executa sobre a quantidade de vezes que ele encontrou a solucao ou falhou. 19:19
def puzz8(maxD,nAmostras):
  tempos = []
  solucionados = []
  solucoes = []
  naoSolucionados = []
  nS = 0
  nNs = 0
  for i in range(nAmostras):
    noInicial = criarNo(geraInicial(),None)
    start_time = timeit.default_timer()
    res,nmov = busca(maxD,noInicial)
    tempo = timeit.default_timer() - start_time
    if res:
      solucoes.append(res)
      print("\n > Solucionado em {} segundos e {} movimentos ".format(tempo,nmov))
      tempos.append(tempo)
      solucionados.append((noInicial.estado,nmov))
      nS += 1 # Solucionados
    else:
      print("\n > Falhou em {} segundos e {} movimentos ".format(tempo,nmov))
      naoSolucionados.append((noInicial.estado,nmov))
      tempos.append(None)
      nNs += 1 # Nao solucionados

  print("\n > Solucionados {} Nao solucionados {} ".format(nS,nNs))
  return tempos, solucionados, naoSolucionados,nS,nNs





movimentos = [i[1] for i in b]
import matplotlib as mpl
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (14,7)
n, b, p = plt.hist(movimentos, 10, facecolor='g', alpha=0.75)
plt.xlabel('Numero de Movimentos')
plt.ylabel('Casos')
plt.title('Histograma de Resolucao do 8-Puzzle')
plt.grid(True)
plt.show()

a,b,c,d,e = puzz8(1500,100)
n, b, p = plt.hist(movimentos, 10, facecolor='b', alpha=0.5, label='Movimentos')
plt.xlabel('Numero de Movimentos')
plt.ylabel('Casos')
plt.title('Histograma de Resolucao do 8-Puzzle')
plt.grid(True)
plt.legend()
plt.show()

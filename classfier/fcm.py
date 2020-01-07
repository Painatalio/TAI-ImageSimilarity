import math

'''
  Classe auxiliar do FCM
'''
class Counts:

    counts = []
    soma = 0

    def __init__(self, nSymbols):
        self.counts = [0] * nSymbols

    def __str__(self):
        return str(self.counts)

    def __repr__(self):
        return str(self.soma)

'''
    Modelo de contexto finito
'''
class Fcm:

    nSymbols = 0
    alphaN = 1
    alphaD = 1
    alpha = 1.0
    counters = {}
    probs = []

    def __init__(self, nSymbols):
        self.nSymbols = nSymbols
        self.probs = [0] * nSymbols

    '''
      Aumenta a frequência de um dado símbolo para um dado contexto(chave).
    '''
    def increment(self, key, symbol):
        if not key in self.counters:
            self.counters[key] = Counts(self.nSymbols)
        self.counters[key].counts[symbol] += 1
        self.counters[key].soma += 1

    '''
      Retorna o número de ocorrências de um símbolo num dado contexto e o total de ocorrências de um dado contexto.
    '''
    def count(self, key, symbol):
        return (self.counters[key].counts[symbol], self.counters[key].soma)

    '''
      Calcula o número de bits necessários para representar um símbolo dado um contexto específico.
    '''
    def bitsNeeded(self, key, symbol, alpha=1):
        count = self.count(key, symbol)

        return -math.log2((count[0] + alpha) / (count[1] + alpha * self.nSymbols))

    def setAlpha(self,n, d):
        self.alphaN = n
        self.alphaD = d
        self.alpha = n/d

    '''
      Calcula a probabildiade de ocorrência dos símbolos dado um contexto.
    '''
    def computeProbs(self, key):
        if(key in self.counters):
            for i in range(self.nSymbols):
                self.probs[i] = ( self.counters[key].counts[i] + self.alpha ) / ( self.counters[key].soma + self.alpha * self.nSymbols )
        else:
            for i in range(self.nSymbols):
                self.probs[i] = 1.0 / self.nSymbols
                
        return self.probs


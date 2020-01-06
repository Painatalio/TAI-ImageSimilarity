



class Alphabet:


    tSymbols = [-1]*256 #Text Symbols  || o simbolo  em T corresponde ao simbolo em C, ou seja, TSymbols[i] = n e Csymbols[n] = i, 
    cSymbols = [-1]*256 #Code Symbols.
    counts = [0]*256
    nSymbols = 0
   
    def __init__(self, refImages, tarImage):

        for img in refImages:
            for line in img:
                for val in line:
                    self.counts[val] = 1

        for line in tarImage:
            for val in line:
                self.counts[val] = 1
        
        for i in range(256):
            if self.counts[i] > 0 :
                self.cSymbols[i] = self.nSymbols
                self.tSymbols[self.nSymbols] = i
                self.nSymbols += 1
        
    def size(self):
        return self.nSymbols
    
    def tSymbolTocSymbol(self, tSymbol):
        return self.cSymbols[tSymbol]

    def cSymbolTotSymbol(self, cSymbol):
        return self.tSymbols[cSymbol]

    



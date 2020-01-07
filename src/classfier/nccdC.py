from fcm import Fcm
from ctx import Ctx
from alphabet import Alphabet
import math
import numpy
import copy
from PIL import Image

class Nccd:

    refCtxs = []

    refFcms = []

    tarCtxs = []

    tarFcms = []

    refCtx = ""

    tarCtx = ""

    gamma = 0.99

    def __init__(self, refCtx, tarCtx, gamma):

        self.refCtx = refCtx
        self.tarCtx = tarCtx
        self.gamma = gamma

    '''
      Realiza o calculo do NCCD
    '''
    def classify(self, refImages, tarImage):

        Cy = self.compress(numpy.array(tarImage.getdata()).reshape(tarImage.size[0], tarImage.size[1]).tolist(), 
                gamma = self.gamma)

        return self.compress(refImages = [ numpy.array(ref.getdata()).reshape(ref.size[0], ref.size[1]).tolist() for ref in refImages ], 
                tarImage = numpy.array(tarImage.getdata()).reshape(tarImage.size[0], tarImage.size[1]).tolist(), 
                gamma = self.gamma)/ Cy


    '''
      Carrega os modelos de contexto finito estáticos
    '''
    def loadReferences(self, refImages):

        for refImage in refImages:
            for ctx in range(len(self.refCtxs)):
                for i in range(len(refImage)):
                    for j in range(len(refImage[i])):
                        self.refFcms[ctx].increment(self.refCtxs[ctx].key(refImage, (i,j)), refImage[i][j])

    '''
      Calcula o número de bits necessários para representar uma imagem dado as imagens de referência e um gamma.
    '''
    def compress(self, tarImage, refImages = [], gamma = 0.99):

        self.tarCtxs = []
        self.tarFcms = []
        self.refCtxs = []
        self.refFcms = []

        alphabet = Alphabet(refImages, tarImage)

        for img in range(len(refImages)):
            for i in range(len(refImages[img])):
                for j in range(len(refImages[img][i])):
                    refImages[img][i][j] = alphabet.tSymbolTocSymbol(refImages[img][i][j])
        
        
        for i in range(len(tarImage)):
            for j in range(len(tarImage[i])):
                tarImage[i][j] = alphabet.tSymbolTocSymbol(tarImage[i][j])
        

        if refImages != []:
            f = open(self.refCtx, "r")
            line  = f.readline()
            while(line != ''):
                self.refCtxs.append(Ctx(line))

                fcm = Fcm(alphabet.size())

                alpha = f.readline().split("/")

                fcm.setAlpha(int(alpha[0]), int(alpha[1]))

                self.refFcms.append(fcm)

                line = f.readline()
            
        f = open(self.tarCtx, "r")
        line  = f.readline()
        while(line != ''):
            self.tarCtxs.append(Ctx(line))

            fcm = Fcm(alphabet.size())

            alpha = f.readline().split("/")

            fcm.setAlpha(int(alpha[0]), int(alpha[1]))

            self.tarFcms.append(fcm)

            line = f.readline()

        self.loadReferences(refImages)


        nBits = 0

        totalWeight = 0

        weightedProbs = [0]*alphabet.size()

        weights = [0]*(len(self.refFcms) + len(self.tarFcms))


        for ctx in range(len(self.refCtxs) + len(self.tarCtxs)):
            weights[ctx] = 1 / (len(self.refCtxs) + len(self.tarCtxs))
            totalWeight += weights[ctx]
        
        for i in range(len(tarImage)):
            for j in range(len(tarImage[i])):

                for s in range(alphabet.size()):
                    weightedProbs[s] = 0

                for ctx in range(len(self.refCtxs)):
                    key = self.refCtxs[ctx].key( tarImage, (i , j))
                    probs = self.refFcms[ctx].computeProbs(key)
                    weights[ctx] /= totalWeight
                    for s in range(alphabet.size()) :
                        weightedProbs[s] += probs[s] * weights[ctx]
                
                for ctx in range(len(self.tarCtxs)):
                    key = self.tarCtxs[ctx].key(tarImage, (i, j))
                    probs = self.tarFcms[ctx].computeProbs(key)
                    weights[len(self.refCtxs) + ctx] /= totalWeight
                    for s in range(alphabet.size()) :
                        weightedProbs[s] += probs[s] * weights[len(self.refCtxs) + ctx]

                nBits += -math.log2(weightedProbs[tarImage[i][j]])

                totalWeight = 0

                for ctx in range(len(self.refCtxs)):

                    weights[ctx] = pow(weights[ctx], gamma) * self.refFcms[ctx].probs[tarImage[i][j]]
                    totalWeight += weights[ctx]

                for ctx in range(len(self.tarCtxs)):

                    weights[len(self.refCtxs) + ctx] = pow(weights[len(self.refCtxs) + ctx], gamma) * self.tarFcms[ctx].probs[tarImage[i][j]]
                    totalWeight += weights[len(self.refCtxs) + ctx]

                for ctx in range(len(self.tarCtxs)):
                    self.tarFcms[ctx].increment(self.tarCtxs[ctx].key(tarImage, (i, j)), tarImage[i][j])
                    
        return nBits
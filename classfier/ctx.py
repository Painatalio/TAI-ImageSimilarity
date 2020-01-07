
'''
Guarda um dado contexto.
'''
class Ctx:

    coords = []

    def __init__(self, line):

        splited_values = line.strip().split(" ")
        for i in range(1, len(splited_values), 2):
            self.coords.append([int(splited_values[i + 1]), int(splited_values[i])]) # [x, y] type of array


    def config(self, line):
        self.coords = []

        splited_values = line.split(" ")
        
        for i in range(0, len(coords), 2):
            self.coords.append([splited_values[i + 1], splited_values[i]]) # [x, y] type of array

    '''
        A chave são os valores dos píxeis.
    '''
    def key(self, img, currrent):

        result = ''

        for p in self.coords:
            i = currrent[0] + p[0]
            j = currrent[1] + p[1]

            if( i < len(img) and i >= 0 and j < len(img[i]) and j >= 0 ):
                result += str(img[i][j])
            
        return result

    def size(self):
        return len(self.coords)

    def getCoords(self):
        return self.coords
import math
import os
import sys
import csv
from PIL import Image
import pre_processing
from ncdC import Ncd
from nccdC import Nccd
import random



'''
Dado um dataset carrega-o usando a técnica de pré-processamento especificada.
'''
def getDataset(dataset, preprocessing):
    
    prepDataset = []
    files = os.listdir(dataset)

    counter = 0
    for f in files:

        fullPath = os.path.join(dataset, f)

        if os.path.isdir(fullPath):
            prepDataset.append([])

            for photo in os.listdir(fullPath):

                photoPath = os.path.join(fullPath, photo)
                if preprocessing["prep"] == "original":
                    prepDataset[counter].append(Image.open(photoPath))
                elif preprocessing["prep"] == "resize":
                    prepDataset[counter].append(pre_processing.resize_image(Image.open(photoPath), preprocessing["ratio"] ))
                elif preprocessing["prep"] == "quantization":
                    prepDataset[counter].append(pre_processing.quantize_image(Image.open(photoPath), preprocessing["n_bits"] ) )
                else:
                    print("Invalid preprocessing step!")
                    sys.exit(1)

            counter += 1

    return prepDataset


'''
Cria o classifier passado por argumento.
'''
def getClassifier(properties):

    if properties["classifier"] == "ncd":
        return Ncd(properties["compressor"])

    if properties["classifier"] == "nccd":
        return Nccd(properties["ctx"], properties["ctx"], properties["gamma"])



'''
Dado um conjunto de classificações calcula o rácio de classificações erradas.
'''
def getError(classifications):
    errors = 0
    for i in range(len(classifications)):
        for j in range(len(classifications[i])):
            if i != classifications[i][j]:
                errors += 1

    return errors/(len(classifications) * len(classifications[0]))

'''
Pasta onde se encontra o dataset
'''
dataset = "orl_faces"

'''
Técnicas de préprocessamento utilizadas.
'''
preprocessing = [ 
    #original image
    {"prep" : "original", "ratio":1},
    # resized and quantized
    {"prep" : "resize", "ratio": 0.5}, 
    {"prep" : "resize", "ratio": 0.25}, 
    {"prep" : "resize", "ratio": 0.1}, 
    {"prep" : "quantization", "n_bits" : 4},
    {"prep" : "quantization", "n_bits" : 6}
    ]

'''
Classificadores Utilizados.
'''
classifiers = [
    {"classifier": "ncd", "compressor" : "gzip" }, 
    {"classifier": "ncd", "compressor" : "bzip2" },    
    {"classifier": "ncd", "compressor" : "lzma" },
    {"classifier": "ncd", "compressor" : "png" },
    {"classifier": "ncd", "compressor" : "jpeg" },
    {"classifier": "nccd", "ctx" : "ctx1", "gamma" : 0.99 }
    ]

'''
Matriz que guarda os erros de todas as combinações preprocessing x classifiers
'''
allErrors = []

'''
Ficheiro no qual se vai guardar os resultados obtidos
'''
output_file = open('output_6.csv','w') 
writer = csv.writer(output_file, delimiter=',')
writer.writerow(["Resize/Quantization", "Ratio/N_Bits", "Classifier", "Compressor/Ctx", "Error"])



'''
Obtenção da matriz de resultados com recurso a uma abordagem
semelhante a k-fold cross validation.
'''
for p in range(len(preprocessing)):
    prepDataset = getDataset(dataset, preprocessing[p])

    leap = math.floor(len(prepDataset[0])/5)

    allErrors.append([])

    for c in range(len(classifiers)):

        value_key_preprocessing = "n_bits" if "n_bits" in preprocessing[p] else "ratio"
        value_key_classifier = "ctx" if "ctx" in classifiers[c] else "compressor"

        if(classifiers[c]["classifier"] == "ncd"):
            print("Classifing using ", classifiers[c]["classifier"], " with compressor ", classifiers[c]["compressor"], 
            "\nand Preprocessing ", preprocessing[p]["prep"], " with value ", preprocessing[p][value_key_preprocessing])

        elif(classifiers[c]["classifier"] == "nccd"):
            print("Classifing using ", classifiers[c]["classifier"], " with context ", classifiers[c]["ctx"], 
            "\nand Preprocessing ", preprocessing[p]["prep"], " with value ", preprocessing[p][value_key_preprocessing])

        errors = []
        if classifiers[c]["classifier"] == "nccd" :

            classifications = []
            '''
              Divisão do Dataset
            '''
            X_train = [ x[0:leap] for x in prepDataset[0:2] ]

            X_test = [ x[leap:] for x in prepDataset[0:2] ]

            for i in range(len(X_test)):
                classifications.append([])
                for j in range(len(X_test[i])):
                    photo = X_test[i][j]
                    compressSpace = []

                    for train_set in X_train:
                        classifier = getClassifier(classifiers[c])
                        #Obtém o min NCCD para a compressão das fotos de referência de todos os sujeitos e da imagem de teste y
                        compressSpace.append(classifier.classify(train_set, photo))
                        del classifier
                    #atribui o menor NCCD como sendo a classificação feita para  a imagem y
                    classifications[i].append(compressSpace.index(min(compressSpace)))
            #Guarda os erro para o respetivo k (neste caso só é 1)
            errors.append(getError(classifications))

        else:
            classifier = getClassifier(classifiers[c])
            for k in range(0,5):
            
                print("\t  k=", k)

                classifications = []
                '''
                  Divisão do dataset.
                '''
                X_train = [ x[k*leap:k*leap+leap] for x in prepDataset ]

                X_test = [ [ *x[0:k*leap], *x[k*leap+leap:] ] for x in prepDataset ]
                for i in range(len(X_test)):
                    classifications.append([])
                    for j in range(len(X_test[i])):
                        compressSpace = []

                        for train_set in X_train:
                            #Obtém o min NCD para a compressão das fotos de referência de todos os sujeitos e da imagem de teste y  
                            compressSpace.append(classifier.classify(train_set, X_test[i][j]))

                        #atribui o menor NCD como sendo a classificação feita para  a imagem y
                        classifications[i].append(compressSpace.index(min(compressSpace)))

                #Guarda os erro para o respetivo k
                errors.append(getError(classifications))
        '''
          Guarda o erro médio para o classifcador x preprocessing
        '''
        allErrors[p].append(sum(errors)/len(errors))
        
        writer.writerow([preprocessing[p]["prep"], preprocessing[p][value_key_preprocessing], classifiers[c]["classifier"], classifiers[c][value_key_classifier], sum(errors)/len(errors)])
            
min_errors = [ min(x) for x in allErrors]

best_preprocessing = min_errors.index(min(min_errors))

best_classifier = allErrors[best_preprocessing].index(min(allErrors[best_preprocessing]))

print("The best Combination is:\nPreprocessing with ", preprocessing[best_preprocessing], "\nClassification with ", classifiers[best_classifier])

            
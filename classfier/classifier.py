import math
import os
import sys
import csv
from PIL import Image
import pre_processing
from ncdC import Ncd
from nccdC import Nccd
import random

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
                if preprocessing == "noPrep":
                    prepDataset[counter].append(photoPath)
                elif preprocessing["prep"] == "resize":
                    prepDataset[counter].append(pre_processing.resize_image(Image.open(photoPath), preprocessing["ratio"] ))
                elif preprocessing["prep"] == "quantization":
                    prepDataset[counter].append(pre_processing.quantize_image(Image.open(photoPath), preprocessing["n_bits"] ) )
                else:
                    print("Invalid preprocessing step!")
                    sys.exit(1)

            counter += 1

    return prepDataset

def getClassifier(properties, preprocessing):

    if properties["classifier"] == "ncd":
        return Ncd(properties["compressor"])

    if properties["classifier"] == "nccd":
        return Nccd(properties["ctx"], properties["ctx"], properties["gamma"])

def getError(classifications):
    errors = 0
    for i in range(len(classifications)):
        for j in range(len(classifications[i])):
            if i != classifications[i][j]:
                errors += 1

    return errors/(len(classifications) * len(classifications[0]))


dataset = "orl_faces"

quantization_levels = [2, 4, 8, 16, 32, 64]
resize_ratios = [0.5, 0.25, 0.10]

preprocessing = [ 
    #{"prep" : "resize", "ratio": 0.5} 
    {"prep" : "resize", "ratio": 0.25}, 
    #{"prep" : "resize", "ratio": 0.1}, 
    #{"prep" : "quantization", "n_bits" : 4},
    #{"prep" : "quantization", "n_bits" : 6},
    ]

classifiers = [
    #{"classifier": "ncd", "compressor" : "gzip" }, 
    #{"classifier": "ncd", "compressor" : "bzip2" },    
    #{"classifier": "ncd", "compressor" : "lzma" },
    {"classifier": "ncd", "compressor" : "png" },
    {"classifier": "ncd", "compressor" : "jpeg" },
    #{"classifier": "nccd", "ctx" : "ctx1" },
    #{"classifier": "nccd", "ctx" : "ctx2" }
    ]

allErrors = []

output_file = open('output_2.csv','w') 
writer = csv.writer(output_file, delimiter=',')
writer.writerow(["Resize/Quantization", "Ratio/N_Bits", "Classifier", "Compressor/Ctx", "Error"])
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
            print("Classifing using ", classifiers[c]["classifier"], " with compressor ", classifiers[c]["ctx"], 
            "\nand Preprocessing ", preprocessing[p]["prep"], " with value ", preprocessing[p][value_key_preprocessing])

        classifier = getClassifier(classifiers[c], preprocessing[p])
        errors = []
        for k in range(0,5):
            print("\t  k=", k)
            classifications = []

            X_train = [ x[k*leap:k*leap+leap] for x in prepDataset ]

            X_test = [ [ *x[0:k*leap], *x[k*leap+leap:] ] for x in prepDataset ]
            for i in range(len(X_test)):
                classifications.append([])
                for j in range(len(X_test[i])):
                    photo = X_test[i][j]
                    compressSpace = []

                    for train_set in X_train:
                        compressSpace.append(classifier.classify(train_set, photo))

                    classifications[i].append(compressSpace.index(min(compressSpace)))
            errors.append(getError(classifications))
        allErrors[p].append(sum(errors)/len(errors))
        
        writer.writerow([preprocessing[p]["prep"], preprocessing[p][value_key_preprocessing], classifiers[c]["classifier"], classifiers[c][value_key_classifier], sum(errors)/len(errors)])
            
min_errors = [ min(x) for x in allErrors]

best_preprocessing = min_errors.index(min(min_errors))

best_classifier = allErrors[best_preprocessing].index(min(allErrors[best_preprocessing]))

print("The best Combination is:\nPreprocessing with ", preprocessing[best_preprocessing], "\nClassification with ", classifiers[best_classifier])

            
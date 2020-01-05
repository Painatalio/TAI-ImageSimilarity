import os


class Nccd:

    ctxFile = ''
    preprocessingFlag = ''

    def __init__(self, ctxFile, preprocessing):
        self.ctxFile = ctxFile
        if preprocessing["prep"] == "resize":
            self.preprocessingFlag = " -R " + str(preprocessing["ratio"])
        elif preprocessing["prep"] == "quantization":
            self.preprocessingFlag = " -q " + str(preprocessing["n_bits"])

    def classify(self, train_set, test_image):
        spaceOcupied = []
        for train_image in train_set:
            CxCommand = "./ImgCondComp -tc " + self.ctxFile + " -t " + train_image + self.preprocessingFlag
            CyCommand = "./ImgCondComp -tc " +  self.ctxFile + " -t " + test_image + self.preprocessingFlag
            CxyCommand = "./ImgCondComp -rc " + self.ctxFile + " -r " + train_image + " -tc " + self.ctxFile + " -t " + test_image + self.preprocessingFlag

            Cx = int(os.popen( CxCommand).read())
            Cy = int(os.popen( CyCommand).read())
            Cxy = int(os.popen( CxyCommand).read())

            spaceOcupied.append(Cxy/max(Cx,Cy))


        return(min(spaceOcupied))
            





import os


class Nccd:

    ctxFile = ''

    def __init__(self, ctxFile, preprocessing):
        self.ctxFile = ctxFile

    def classify(self, train_set, test_image):
        spaceOcupied = []
        for train_image in train_set:
            CxCommand = "./ImgCondComp -tc " + self.ctxFile + " -t " + train_image
            CyCommand = "./ImgCondComp -tc " +  self.ctxFile + " -t " + test_image
            CxyCommand = "./ImgCondComp -rc " + self.ctxFile + " -r " + train_image + " -tc " + self.ctxFile + " -t " + test_image

            Cx = int(os.popen( CxCommand).read())
            Cy = int(os.popen( CyCommand).read())
            Cxy = int(os.popen( CxyCommand).read())

            spaceOcupied.append(Cxy/max(Cx,Cy))


        return(min(spaceOcupied))
            





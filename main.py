from functions import *

imagesFolderPath = "./Images"
referenceImage = ""

compareSetNumber = 5 
compareMinSimilarity = 10
compareNumberOfComparations = 50

def main():
     descargar_imagenes_csv('inditextech_hackupc_challenge_images.csv', './Images')

    imagesInFolder = os.listdir(imagesFolderPath)

    for image in imagesInFolder:
        if compareReferenceWithImage(referenceImage, image):
            saveImage(image)

if __name__ == "__main__":
    main()
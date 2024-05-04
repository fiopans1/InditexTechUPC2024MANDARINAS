from functions import *

imagesFolderPath = "./Images/"
similarImagesFolderPath = "./SimilarImages/"
referenceImage = ""

compareSetNumber = 5 
compareMinSimilarity = 10
compareNumberOfComparations = 50

def main():
    descargar_imagenes_csv_ultima_columna('inditextech_hackupc_challenge_images.csv', './Images')

    # imagesInFolder = os.listdir(imagesFolderPath)

    # for image in imagesInFolder:
    #     if (image.endswith(".png")):
    #         imagen_pillow = Image.open(imagesFolderPath + image)
    #         if compareReferenceWithImage(referenceImage, imagen_pillow):
    #             saveImage(imagen_pillow, similarImagesFolderPath + image)


if __name__ == "__main__":
    main()
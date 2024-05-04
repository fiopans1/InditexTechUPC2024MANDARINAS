from functions import *
from recorte import *

imagesFolderPath = "./Images/"
similarImagesFolderPath = "./SimilarImages/"
referenceImage = "0722407802_6_1_1.png"

referenceImage2 = "./Images/2335330658_3_1_1.png"
referenceImage3 = "./Images/2910009051_3_1_1.png"

compareSetNumber = 5 
compareMinSimilarity = 10
compareNumberOfComparations = 50

def main():
    #descargar_imagenes_csv('inditextech_hackupc_challenge_images.csv', './Images')
    
    imagen_reference_pillow = Image.open(imagesFolderPath + referenceImage)
    imagen_reference_cv2 = cv2.imread(imagesFolderPath + referenceImage, 1)


    imagesInFolder = os.listdir(imagesFolderPath)

    for image in imagesInFolder:
        if (image.endswith(".png")):
            imagen_pillow = Image.open(imagesFolderPath + image)
            imagen_cv2 = cv2.imread(imagesFolderPath + image, 1)

            if compareReferenceWithImage(referenceImage, imagen_pillow):
                #saveImage(imagen_pillow, similarImagesFolderPath + image)
                #recortar_contornos(imagen_cv2)

                diferencia = compararHistogramas(imagen_reference_cv2, imagen_cv2)
                print("La diferencia de color medio entre la imagen de referencia y: "+ image +" imágenes es:", diferencia)


if __name__ == "__main__":
    main()
from functions import *
from recorte import *

imagesFolderPath = "./Images/"
similarImagesFolderPath = "./SimilarImages/"
referenceImage = "3153002630_6_1_1.png"

compareSetNumber = 5 
compareMinSimilarity = 10
compareNumberOfComparations = 50

def main():
    #descargar_imagenes_csv('inditextech_hackupc_challenge_images.csv', './Images')
    
    imagen_reference_cv2 = cv2.imread(imagesFolderPath + referenceImage, 1)

    imagesInFolder = os.listdir(imagesFolderPath)
    maskImgRef = crearMascara(imagen_reference_cv2)

    bestImages = []
    for image in imagesInFolder:
        if (image.endswith(".png")):
            imagen_cv2 = cv2.imread(imagesFolderPath + image, 1)

            maskImgCompare = crearMascara(imagen_cv2)

            if compareReferenceWithImage(referenceImage, imagen_cv2, maskImgRef, maskImgCompare) > 0.1:
                imagen_cv2 = cv2.resize(imagen_cv2, (1024,1024))
                bestImages.append(imagen_cv2)
    
    i = 0
    bestImagesCount = len(bestImages)
    for image in bestImages:
        i += 1
        cv2.imshow(str(i) + " de " + str(bestImagesCount) + "bestImages", image)
        cv2.waitKey(0)

if __name__ == "__main__":
    main()
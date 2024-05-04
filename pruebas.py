import numpy as np
from skimage import io
from skimage.metrics import structural_similarity as compare_ssim
import cv2


def fillGaps(imagen_umbralizada):
    if len(imagen_umbralizada.shape) > 2:
        imagen_umbralizada = cv2.cvtColor(imagen_umbralizada, cv2.COLOR_BGR2GRAY)
    # Encontrar todos los contornos en la imagen
    contornos, _ = cv2.findContours(imagen_umbralizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Crear una imagen en negro del mismo tamaño que la imagen de entrada
    imagen_rellena = np.zeros_like(imagen_umbralizada)
    
    # Dibujar todos los contornos encontrados en blanco
    cv2.drawContours(imagen_rellena, contornos, -1, (255), thickness=cv2.FILLED)
    
    return imagen_rellena

def eliminar_contorno(imagen):
    _, imagen_umbralizada = cv2.threshold(imagen, 200, 255, cv2.THRESH_BINARY_INV)
    image = fillGaps(imagen_umbralizada)

        # Encontrar los contornos
    contornos, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Crear una imagen en blanco del mismo tamaño que la imagen original
    imagen_contornos = np.zeros_like(image)

    # Dibujar los contornos en la imagen en blanco
    cv2.drawContours(imagen_contornos, contornos, -1, 255, 10)

    return imagen_contornos


# Cargar las imágenes
imagen1 = eliminar_contorno(cv2.imread('/Users/fiopans1/git/InditexTechUPC2024MANDARINAS/Images/4285498401_3_1_1.png'))
imagen2 = eliminar_contorno(cv2.imread('/Users/fiopans1/git/InditexTechUPC2024MANDARINAS/Images/0039678800_3_1_1.png'))

# Asegurarse de que las imágenes tienen el mismo tamaño
if imagen1.shape != imagen2.shape:
    raise ValueError("Las imágenes deben tener el mismo tamaño")

# Calcular el SSIM entre las dos imágenes
ssim = compare_ssim(imagen1, imagen2)

print(f"El índice de similitud estructural entre las imágenes es: {ssim}")
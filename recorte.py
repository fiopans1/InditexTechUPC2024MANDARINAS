import cv2
from matplotlib import pyplot as plt
import numpy as np

def recortar_contornos(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    plt.imshow(imagen_gris, cmap='gray')
    plt.show()
    # Aplicar el filtro de Canny para detectar bordes
    bordes = cv2.Canny(imagen_gris, 30, 200)

    # Encontrar los contornos
    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Recortar cada contorno y guardar las imágenes recortadas en una lista
    imagenes_recortadas = []
    for contorno in contornos:
        x, y, w, h = cv2.boundingRect(contorno)
        imagen_recortada = imagen[y:y+h, x:x+w]
        imagenes_recortadas.append(imagen_recortada)

    return imagenes_recortadas


def unir_contornos(imagen_contornos):
    # Definir el kernel para la dilatación
    kernel = np.ones((5,5),np.uint8)

    # Aplicar la dilatación a la imagen de contornos
    imagen_contornos_unidos = cv2.dilate(imagen_contornos, kernel, iterations = 1)

    return imagen_contornos_unidos



def eliminar_fondo_y_quedarse_con_borde_externo(imagen):
    # Aplicar un filtro gaussiano
    imagen_suavizada = cv2.GaussianBlur(imagen, (5, 5), 0)

    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen_suavizada, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Imagen sin fondo', imagen_gris)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # Aplicar un umbral para convertir el fondo blanco en negro y el objeto en blanco
    _, imagen_umbralizada = cv2.threshold(imagen_gris, 200, 255, cv2.THRESH_BINARY_INV)

    # Encontrar los contornos
    contornos, _ = cv2.findContours(imagen_umbralizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 # Crear una imagen en blanco del mismo tamaño que la imagen original
    imagen_contornos = np.zeros_like(imagen)

    # Dibujar los contornos en la imagen en blanco
    cv2.drawContours(imagen_contornos, contornos, -1, (255,255,255), 1)

    # Mostrar la imagen
    cv2.imshow('Contornos', unir_contornos(imagen_contornos))
    cv2.waitKey(0)
    cv2.destroyAllWindows()



    # Aplicar la máscara a la imagen
    imagen_sin_fondo = cv2.bitwise_and(imagen, unir_contornos(imagen_contornos))

    return imagen_sin_fondo

# Uso de la función
imagen = cv2.imread('/Users/fiopans1/git/InditexTechUPC2024MANDARINAS/Images/0722407802_3_1_1.png')
imagen_sin_fondo = eliminar_fondo_y_quedarse_con_borde_externo(imagen)
cv2.imshow('Imagen sin fondo', imagen_sin_fondo)
cv2.waitKey(0)
cv2.destroyAllWindows()
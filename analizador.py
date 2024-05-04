import cv2
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

    # Aplicar un umbral para convertir el fondo blanco en negro y el objeto en blanco
    _, imagen_umbralizada = cv2.threshold(imagen_gris, 200, 255, cv2.THRESH_BINARY_INV)
    imagen_umbralizada = cv2.GaussianBlur(imagen_umbralizada, (5, 5), 0)
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

    return unir_contornos(imagen_contornos)

def calcular_hu_moments(imagen):
    # Aplicar el filtro de Canny para detectar bordes
    bordes = cv2.Canny(eliminar_fondo_y_quedarse_con_borde_externo(imagen), 30, 200)

    # Encontrar los contornos
    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contorno_max = max(contornos, key=cv2.contourArea)

    # Calcular los momentos de Hu para el contorno de mayor área
    hu_moments = cv2.HuMoments(cv2.moments(contorno_max)).flatten()

    return hu_moments

# Leer las dos imágenes
imagen1 = cv2.imread('/Users/fiopans1/git/InditexTechUPC2024MANDARINAS/Images/0722407802_3_1_1.png')
imagen2 = cv2.imread('/Users/fiopans1/git/InditexTechUPC2024MANDARINAS/Images/0722407802_6_1_1.png')

# # Calcular los momentos de Hu de cada imagen
# hu_moments1 = calcular_hu_moments(imagen1)
# hu_moments2 = calcular_hu_moments(imagen2)
# print(hu_moments1)
# print(hu_moments2)
# # Comparar los momentos de Hu
# # Aquí simplemente estamos restando los momentos de Hu y tomando el valor absoluto
# # Puedes usar cualquier métrica de distancia que prefieras
# diferencias = [np.abs(hm1 - hm2) for hm1, hm2 in zip(hu_moments1, hu_moments2)]

# # Imprimir las diferencias
# for i, diferencia in enumerate(diferencias):
#     print(f'Diferencia en los momentos de Hu para el contorno {i+1}: {diferencia}')
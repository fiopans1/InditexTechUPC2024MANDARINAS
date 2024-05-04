import cv2
import numpy as np

def calcular_hu_moments(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar el filtro de Canny
    bordes = cv2.Canny(imagen_gris, 30, 200)

    # Encontrar los contornos
    contornos, _ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Calcular los momentos de Hu para cada contorno y aplanarlos
    hu_moments = [cv2.HuMoments(cv2.moments(contorno)).flatten() for contorno in contornos]

    return hu_moments

# Leer las dos imágenes
imagen1 = cv2.imread('imagen1.jpg')
imagen2 = cv2.imread('imagen2.jpg')

# Calcular los momentos de Hu de cada imagen
hu_moments1 = calcular_hu_moments(imagen1)
hu_moments2 = calcular_hu_moments(imagen2)

# Comparar los momentos de Hu
# Aquí simplemente estamos restando los momentos de Hu y tomando el valor absoluto
# Puedes usar cualquier métrica de distancia que prefieras
diferencias = [np.abs(hm1 - hm2) for hm1, hm2 in zip(hu_moments1, hu_moments2)]

# Imprimir las diferencias
for i, diferencia in enumerate(diferencias):
    print(f'Diferencia en los momentos de Hu para el contorno {i+1}: {diferencia}')
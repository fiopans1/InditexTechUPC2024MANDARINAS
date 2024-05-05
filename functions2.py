import os
import numpy as np
from skimage import io
from skimage.metrics import structural_similarity as ssim
import cv2

def eliminar_contorno(imagen):
    imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    imagen = cv2.resize(imagen, (256,256))
    _, imagen_umbralizada = cv2.threshold(imagen, 254, 255, cv2.THRESH_BINARY)
    invertida = 255 - imagen_umbralizada
    contornos, _ = cv2.findContours(invertida, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    imagen_contornos = np.zeros_like(invertida)
    cv2.drawContours(imagen_contornos, contornos, -1, 255, thickness=cv2.FILLED)
    #resultado = cv2.bitwise_and(imagen, imagen, mask=imagen_contornos)
    # cv2.imshow('Imagen', imagen_contornos)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return imagen_contornos

#definimos umbral
umbral = 0.85



# Cargar la plantilla
imagen_original = cv2.imread('./Images/0039678800_3_1_1.png')
plantilla = eliminar_contorno(imagen_original)

# Carpeta de imágenes
carpeta_imagenes = './images'
lista_coincidencias = []
# Recorrer todas las imágenes en la carpeta
for nombre_imagen in os.listdir(carpeta_imagenes):
    # Verificar si el archivo es un PNG
    if nombre_imagen.endswith('.png'):
        # Cargar la imagen
        imagen_a_guardar=cv2.imread(os.path.join(carpeta_imagenes, nombre_imagen))
        imagen_a_comprobar = eliminar_contorno(imagen_a_guardar)
        # Asegurarse de que las imágenes tienen el mismo tamaño
        if imagen_a_comprobar is not None:
            sim = ssim(plantilla,imagen_a_comprobar)
            if (sim>umbral):
                lista_coincidencias.append((imagen_a_guardar,sim))
print(len(lista_coincidencias))
lista_coincidencias = sorted(lista_coincidencias, key=lambda x: x[1])
for element in lista_coincidencias:
    print(element[1])
    cv2.imshow('Imagen', element[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    


# for pt in zip(*loc[::-1]):
#     imagen_coincidencia = imagen[pt[1]:pt[1]+h, pt[0]:pt[0]+w]
#     correlacion = np.corrcoef(imagen.flatten(), imagen_coincidencia.flatten())[0, 1]
#     print(f'Correlación con la imagen original: {correlacion}')

#     # Dibujar un rectángulo alrededor de la coincidencia
#     cv2.rectangle(imagen, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
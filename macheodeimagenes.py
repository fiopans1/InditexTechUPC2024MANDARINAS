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



# Cargar la plantilla
imagen_original = cv2.imread('/Users/fiopans1/git/InditexTechUPC2024MANDARINAS/Images/5536006712_3_1_1.png')
plantilla = eliminar_contorno(imagen_original)
w, h = plantilla.shape

# Carpeta de imágenes
carpeta_imagenes = './images'
lista_coincidencias = []
# Recorrer todas las imágenes en la carpeta
for nombre_imagen in os.listdir(carpeta_imagenes):
    # Verificar si el archivo es un PNG
    if nombre_imagen.endswith('.png'):
        # Cargar la imagen
        imagen1=cv2.imread(os.path.join(carpeta_imagenes, nombre_imagen))
        imagen = eliminar_contorno(imagen1)
        # Usar matchTemplate para encontrar la plantilla en la imagen
        res = cv2.matchTemplate(imagen, plantilla, cv2.TM_CCORR_NORMED)

        # Si hay una coincidencia con un umbral, mostrar la imagen
        umbral = 0.8 
        if np.any(res > umbral):
            # Dibujar un rectángulo alrededor de cada coincidencia
            for pt in zip(*np.where(res >= umbral)[::-1]):
                cv2.rectangle(imagen, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
            lista_coincidencias.append(imagen1)
for element in lista_coincidencias:
    cv2.imshow('Imagen', element)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# for pt in zip(*loc[::-1]):
#     imagen_coincidencia = imagen[pt[1]:pt[1]+h, pt[0]:pt[0]+w]
#     correlacion = np.corrcoef(imagen.flatten(), imagen_coincidencia.flatten())[0, 1]
#     print(f'Correlación con la imagen original: {correlacion}')

#     # Dibujar un rectángulo alrededor de la coincidencia
#     cv2.rectangle(imagen, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

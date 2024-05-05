import requests
import csv
import os
import pandas as pd
from PIL import Image
import io

import cv2

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as image

import skimage as ski

def saveImage(imagen, ruta_guardado):
    try:
        imagen.save(ruta_guardado)
        print("La imagen se ha guardado exitosamente en:", ruta_guardado)
    except Exception as e:
        print("Error al guardar la imagen:", e)

def downloadCsvImages(archivo_csv, directorio_destino):
    # Crear el directorio destino si no existe
    if not os.path.exists(directorio_destino):
        os.makedirs(directorio_destino)
    
    with open(archivo_csv, 'r') as archivo:
        lector_csv = csv.reader(archivo)
        for fila in lector_csv:
            url_imagen = fila[0]
            nombre_archivo = url_imagen.split('/')[-1]
            ruta_guardado = os.path.join(directorio_destino, nombre_archivo)
            
            try:
                respuesta = requests.get(url_imagen, stream=True)
                with open(ruta_guardado, 'wb') as archivo_local:
                    for chunk in respuesta.iter_content(chunk_size=1024):
                        archivo_local.write(chunk)
                print(f"Imagen descargada: {nombre_archivo}")
            except Exception as e:
                print(f"Error al descargar la imagen {nombre_archivo}: {e}")


def descargar_imagenes_csv(ruta_csv, directorio_imagenes):
    # Leer el archivo CSV
    df = pd.read_csv(ruta_csv)

    # Crear un directorio para las imágenes si no existe
    if not os.path.exists(directorio_imagenes):
        os.makedirs(directorio_imagenes)

    # Recorrer cada fila del DataFrame
    for index, row in df.iterrows():
        # Recorrer cada columna de la fila
        for columna in row.index:
            url = row[columna]
            # Verificar si la celda contiene una URL de imagen
            if pd.notnull(url) and url.startswith('http'):
                # Obtener el nombre de la imagen de la URL
                nombre_imagen = url.split('/')[-1]
                # Cambiar la extensión a .png
                nombre_imagen = os.path.splitext(nombre_imagen)[0] + '.png'
                # Crear la ruta completa para guardar la imagen
                ruta_imagen = os.path.join(directorio_imagenes, nombre_imagen)
                # Descargar la imagen
                respuesta = requests.get(url)
                # Abrir la imagen en memoria y guardarla como PNG
                imagen = Image.open(io.BytesIO(respuesta.content))
                imagen.save(ruta_imagen, 'PNG')
def descargar_imagenes_csv_ultima_columna(ruta_csv, directorio_imagenes):
    # Leer el archivo CSV
    df = pd.read_csv(ruta_csv)

    # Crear un directorio para las imágenes si no existe
    if not os.path.exists(directorio_imagenes):
        os.makedirs(directorio_imagenes)

    # Recorrer cada fila del DataFrame
    for index, row in df.iterrows():
        # Seleccionar solo la última columna de la fila
        url = row.iloc[-1]
        # Verificar si la celda contiene una URL de imagen
        if pd.notnull(url) and url.startswith('http'):
            # Obtener el nombre de la imagen de la URL
            nombre_imagen = url.split('/')[-1]
            # Cambiar la extensión a .png
            nombre_imagen = os.path.splitext(nombre_imagen)[0] + '.png'
            # Crear la ruta completa para guardar la imagen
            ruta_imagen = os.path.join(directorio_imagenes, nombre_imagen)
            # Descargar la imagen
            respuesta = requests.get(url)
            # Abrir la imagen en memoria y guardarla como PNG
            imagen = Image.open(io.BytesIO(respuesta.content))
            imagen.save(ruta_imagen, 'PNG')
def plotImage(imageRoute):
    imagen = image.imread(imageRoute)

    # Mostrar la imagen usando matplotlib.pyplot
    plt.imshow(imagen)
    plt.axis('off')  # Desactivar los ejes
    plt.show()

def compareReferenceWithImage(imageReference, imageToCompareWith, maskImgRef, maskImgCompare):
    #saveImage(imagen_pillow, similarImagesFolderPath + image)
    #recortar_contornos(imagen_cv2)
    diferencia = compararHistogramas(imageReference, imageToCompareWith, maskImgRef, maskImgCompare)
    if (diferencia > 0.1):
        print("Diferencia: ", diferencia)
        return diferencia
    return 0
    
def deleteBackground(inImage):
    imageHSV = ski.color.rgb2hsv(inImage)
    
    # Separar las partes de la imagen donde el verde tome ciertos valores de intensidad y saturación.
    lower_mask = imageHSV[:,:,0] > 0.15 # Threshold inferior
    upper_mask = imageHSV[:,:,0] < 0.45 # Threshold superior
    saturation_mask = imageHSV[:,:,1] > 0.35
    
    mask = upper_mask*lower_mask*saturation_mask
    red = inImage[:,:,0]*mask
    green = inImage[:,:,1]*mask
    blue = inImage[:,:,2]*mask
    imagenRopaSeparada = np.dstack((red,green,blue))

    return imagenRopaSeparada

def crearMascara(imagen1):
    imagenEscalaGrises = cv2.cvtColor(imagen1, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imagenEscalaGrises, 0, 230, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    thresh = cv2.resize(thresh, (1024, 1024))  

    thresh = np.uint8(thresh)

    return thresh


def compararHistogramas(imagen1, imagen2, maskRef, maskCompare):
    imagen1 = cv2.resize(imagen1, (1024,1024))
    imagen2 = cv2.resize(imagen2, (1024,1024))

    maskRef = np.uint8(maskRef)
    maskCompare = np.uint8(maskCompare)

    imagen1Histogram = cv2.calcHist([imagen1], [0,1,2], maskRef, [32,32,32], ranges=[0,230,0,230,0,230])
    imagen2Histogram = cv2.calcHist([imagen2], [0,1,2], maskCompare, [32,32,32], ranges=[0,230,0,230,0,230])

    comparationResult = cv2.compareHist(imagen1Histogram, imagen2Histogram, 0)

    return comparationResult
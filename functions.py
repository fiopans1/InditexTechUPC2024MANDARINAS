import requests
import csv
import os

import matplotlib.pyplot as plt
import matplotlib.image as image

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

def plotImage(imageRoute):
    imagen = image.imread(imageRoute)

    # Mostrar la imagen usando matplotlib.pyplot
    plt.imshow(imagen)
    plt.axis('off')  # Desactivar los ejes
    plt.show()
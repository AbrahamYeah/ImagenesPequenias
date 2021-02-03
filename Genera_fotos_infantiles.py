# Se importa la libreria para detectar archivos, crear carpetas etc.
from os import scandir, getcwd, path, mkdir
# Se importa la libreria mas importante, OpenCV2 es con la que procesaremos las imagenes
import cv2
# Se importa la Numpy para analisar patrones de imagenes
import numpy as np 
# Se manda a llamar la libreria para generar la interfaz
import tkinter  as tk
# Se utiliza para renderizar la imagen de una mejor manera
from imutils import resize as rz 
#from imutils import resize as rz 
from tkinter import messagebox

import sys


class Fotos:
    ruta_img_input = "Img_Input"
    ruta_img_output = "Img_Output"
    
    def __init__(self):
        self.instalacion()
        self.Genera_interfaz()

    def Genera_interfaz(self):
        ruta_input = self.ruta_img_input
        ruta_output = self.ruta_img_output
        root = tk.Tk()
        root.config(bd=30)  # borde exterior de 15 píxeles, queda mejor
        root.geometry("400x200+0+0")
        root.title("Generador de fotos tamaño infantil")
        # Tres StringVar para manejar los números y el resultado
        tk.Label(root, text="Ruta de las imagenes a procesar:").pack()
        textInput = tk.Entry(root)
        textInput.textvariable=ruta_input
        textInput.insert(0, self.ruta_img_input)
        textInput.pack()

        tk.Label(root, text="\nRuta de las imagenes terminadas:").pack()
        textOutput = tk.Entry(root)
        textOutput.textvariable=ruta_output
        textOutput.insert(0, self.ruta_img_output)
        textOutput.pack()

        tk.Label(root).pack() # Separador
        tk.Button(root, text="Iniciar", command=lambda : self.actualiza_rutas_boton(textInput.get(),textOutput.get())).pack()
        root.mainloop() 
        
    # Con este metodo, empezamos el procesado de imagenes.

    def actualiza_rutas_boton(self,ruta_in=None,ruta_ou=None):
        if ruta_in is not None:
            self.ruta_img_input = ruta_in
        if ruta_ou is not None:
            self.ruta_img_output = ruta_ou 
        self.Inicia_proceso()
            

    def Inicia_proceso(self):
        imagenes = self.ls(self.ruta_img_input)
        if len(imagenes) > 0:
            messagebox.showinfo(message="El proceso puede demorar algunos minutos, por favor espere.", title="Inicia proceso")
            for foto in imagenes:
                print(foto)
                self.Recorta_caras_tamano_infantil(foto)
            print("Terminamos, ve a ver los resultados a {}".format(self.ruta_img_output))
            messagebox.showinfo(message="Terminamos, ve a ver los resultados a {}".format(self.ruta_img_output), title="¡Exito!")
        else:
            messagebox.showinfo(message="No hay archivos en la carpeta seleccionada {}".format(self.ruta_img_input), title="Error")

    # Con este metodo validamos si ya existen las carpetas de imagenes con las que vamos a trabajr
    def instalacion(self):
        if path.isdir(self.ruta_img_input) and path.isdir(self.ruta_img_output):
            print('Las carpetas existen.')
        else:
            print('La carpeta no existe, procederemos a crearlas.')
            mkdir(self.ruta_img_input)
            mkdir(self.ruta_img_output)
            print('Las carpetas se crearon de manera exitosa.')

    # Se extraen todos los nombres de documentos de una ruta.
    def ls(self,ruta):
        self.ruta = self.ruta_img_input
        return [arch.name for arch in scandir(self.ruta) if arch.is_file()]
   
    # Este metododo es el que nos hara el trabajo de dar formato infantil a las fotos
    def Recorta_caras_tamano_infantil(self,foto):
        cascada_rostro = cv2.CascadeClassifier('src/haarcascade_frontalface_alt.xml')
        # Si utilizas otro clasificador o lo tienes guardado en un directorio diferente al de este script python,
        # tendrás que cambiar 'haarcascade_frontalface_alt.xml' por el path a tu fichero xml.
        self.foto = foto
        imagen = self.foto
        nombre_img_arr= imagen.split('.') # Separamos el nombre de la imagen de la extención
        imagen_fin = '{}_RC.PNG'.format(nombre_img_arr[0],nombre_img_arr[1]) # Preparamos el nombre de resultado
        img = cv2.imread('{}\{}'.format(self.ruta_img_input,imagen)) # Se lee la imagen con la ruta especificada
        imageAux = img.copy() # Copiamos la imagen para poder recortarla despues
        img_gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Se pone la imagen a blanco y negro para identificar mejor el rostro
        # Nota: la imagen de ejemplo que hemos utilizado para el tutorial ya está en blanco y negro,
        # por lo que no sería necesario convertirla. Lo he hecho igualmente por si más adelante queréis
        # probar con una imagen en color.
        #Buscamos los rostros:
        coordenadas_rostros = cascada_rostro.detectMultiScale(img_gris, 1.1, 5)
        anchos = []
        altos = []
        #Ahora recorremos el array 'coordenadas_rostros' y dibujamos los rectángulos sobre la imagen original:
        #Primero evaluamos los anchos de los rostros
        for (x,y,ancho, alto) in coordenadas_rostros:
            anchos.append(ancho)
            altos.append(alto)
            try:
                for (x,y,ancho, alto) in coordenadas_rostros:
                    if max(anchos) == ancho:
                        if max(anchos) > 760:
                            extrae_cabello = int(round(max(anchos)*1.28))-alto
                            extrae_cuello= int(round(max(altos)*1.27))-ancho
                            vx = int(round(x*1.4))-x
                            vy = int(round(y*1.95))-y
                            #y luego el area que queremos tomarl
                            print(alto,ancho)
                            print(vx,vy,x,y)
                            cv2.rectangle(img, ( x - vx , y - vy) , (x+ancho+extrae_cuello , y+alto+extrae_cabello) , (0,0,255) , 3)
                            valor_x = (x - vx) 
                            valor_y = (y - vy)
                            valor_x_a = (x+ancho+extrae_cuello)
                            valor_y_a = (y+alto+extrae_cabello)
                            img_rectable = imageAux[valor_y:valor_y_a,valor_x:valor_x_a]
                            rostro = rz(img_rectable, width=945, height=1122)
                            height, widht, canal = rostro.shape 
                            if int(height-1122) < 0:
                                extrae_cabello = int(round(max(anchos)*1.55))-alto
                                extrae_cuello= int(round(max(altos)*1.27))-ancho
                                vx = int(round(x*1.3))-x
                                vy = int(round(y*1.95))-y
                                #y luego el area que queremos tomarl
                                print(alto,ancho)
                                print(vx,vy,x,y)
                                cv2.rectangle(img, ( x - vx , y - vy) , (x+ancho+extrae_cuello , y+alto+extrae_cabello) , (0,0,255) , 3)
                                valor_x = (x - vx)
                                valor_y = (y - vy)
                                valor_x_a = (x+ancho+extrae_cuello)
                                valor_y_a = (y+alto+extrae_cabello)
                                img_rectable = imageAux[valor_y:valor_y_a,valor_x:valor_x_a]
                                rostro = rz(img_rectable, width=945, height=1122)
                        elif max(anchos) < 760 and max(anchos) > 650 :
                            extrae_cabello = int(round(max(anchos)*1.3))-alto
                            extrae_cuello= int(round(max(altos)*1.27))-ancho
                            vx = int(round(x*1.3))-x
                            vy = int(round(y*1.75))-y
                            #y luego el area que queremos tomarl
                            print(alto,ancho)
                            print(vx,vy,x,y)
                            cv2.rectangle(img, ( x - vx , y - vy) , (x+ancho+extrae_cuello , y+alto+extrae_cabello) , (0,0,255) , 3)
                            valor_x = (x - vx) 
                            valor_y = (y - vy)
                            valor_x_a = (x+ancho+extrae_cuello)
                            valor_y_a = (y+alto+extrae_cabello)
                            img_rectable = imageAux[valor_y:valor_y_a,valor_x:valor_x_a]
                            rostro = rz(img_rectable, width=945, height=1122)
                            height, widht, canal = rostro.shape 
                            if int(height-1122) < 0:
                                extrae_cabello = int(round(max(anchos)*1.55))-alto
                                extrae_cuello= int(round(max(altos)*1.27))-ancho
                                vx = int(round(x*1.3))-x
                                vy = int(round(y*1.95))-y
                                #y luego el area que queremos tomarl
                                print(alto,ancho)
                                print(vx,vy,x,y)
                                cv2.rectangle(img, ( x - vx , y - vy) , (x+ancho+extrae_cuello , y+alto+extrae_cabello) , (0,0,255) , 3)
                                valor_x = (x - vx)
                                valor_y = (y - vy)
                                valor_x_a = (x+ancho+extrae_cuello)
                                valor_y_a = (y+alto+extrae_cabello)
                                img_rectable = imageAux[valor_y:valor_y_a,valor_x:valor_x_a]
                                rostro = rz(img_rectable, width=945, height=1122)
                        else:
                            extrae_cabello = int(round(max(anchos)*1.35))-alto
                            extrae_cuello= int(round(max(altos)*1.27))-ancho
                            vx = int(round(x*1.25))-x
                            vy = int(round(y*1.7))-y
                            #y luego el area que queremos tomarl
                            print(alto,ancho)
                            print(vx,vy,x,y)
                            cv2.rectangle(img, ( x - vx , y - vy) , (x+ancho+extrae_cuello , y+alto+extrae_cabello) , (0,0,255) , 3)
                            valor_x = (x - vx) 
                            valor_y = (y - vy)
                            valor_x_a = (x+ancho+extrae_cuello)
                            valor_y_a = (y+alto+extrae_cabello)
                            img_rectable = imageAux[valor_y:valor_y_a,valor_x:valor_x_a]
                            rostro = rz(img_rectable, width=945, height=1122)
                            height, widht, canal = rostro.shape 
                            if int(height-1122) < 0:
                                extrae_cabello = int(round(max(anchos)*1.55))-alto
                                extrae_cuello= int(round(max(altos)*1.27))-ancho
                                vx = int(round(x*1.3))-x
                                vy = int(round(y*1.95))-y
                                #y luego el area que queremos tomarl
                                print(alto,ancho)
                                print(vx,vy,x,y)
                                cv2.rectangle(img, ( x - vx , y - vy) , (x+ancho+extrae_cuello , y+alto+extrae_cabello) , (0,0,255) , 3)
                                valor_x = (x - vx)
                                valor_y = (y - vy)
                                valor_x_a = (x+ancho+extrae_cuello)
                                valor_y_a = (y+alto+extrae_cabello)
                                img_rectable = imageAux[valor_y:valor_y_a,valor_x:valor_x_a]
                                rostro = rz(img_rectable, width=945, height=1122)

                        height, widht, canal = rostro.shape 
                        rostro2 = rostro[abs(int(height-1122)):height,0:widht]
                if cv2.imwrite('{}\{}'.format(self.ruta_img_output,imagen_fin),rostro2) is True:
                    img = None
                    rostro = None
                else:
                     print("No se pudo guardar la imagen")
            except:
                cv2.imwrite('{}\FALLO_{}'.format(self.ruta_img_output,imagen_fin),imageAux)
                print("No se detecto rostro, la imagen se guardo en {}\FALLO_{}".format(self.ruta_img_output,imagen_fin))
    # Con este metodo se genera la vista para interactuar con las variables de rutas

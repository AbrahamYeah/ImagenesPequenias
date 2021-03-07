
from Genera_fotos_infantiles import *
#from imutils import resize as rz 
from tkinter import messagebox
# Se manda a llamar la libreria para generar la interfaz
import tkinter  as tk

class Interfaz(Fotos):

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

import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from core.organizador import organizar_archivos

def seleccionar_carpeta(carpeta_origen):
    ruta = filedialog.askdirectory()
    if ruta:
        carpeta_origen.set(ruta)

def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("Organizador de Archivos con IA")
    ventana.geometry("700x500")

    # StringVar asociado a la ventana raíz
    carpeta_origen = tk.StringVar()

    tk.Label(ventana, text="Carpeta de origen:").pack(pady=5)
    tk.Entry(ventana, textvariable=carpeta_origen, width=60).pack(pady=5)
    tk.Button(
        ventana,
        text="Seleccionar Carpeta",
        command=lambda: seleccionar_carpeta(carpeta_origen)
    ).pack(pady=5)

    progreso = ttk.Progressbar(ventana, length=500, mode="determinate")
    progreso.pack(pady=10)

    salida = scrolledtext.ScrolledText(ventana, width=80, height=15)
    salida.pack(pady=10)

    tk.Button(
        ventana,
        text="Organizar Archivos",
        command=lambda: organizar_archivos(carpeta_origen.get(), progreso, salida, ventana),
        bg="lightblue"
    ).pack(pady=10)

    ventana.mainloop()
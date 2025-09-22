import os
import shutil
from tkinter import messagebox
from core.clasificador import clasificar_texto, clasificar_imagen, categorias_texto, categorias_imagen

def organizar_archivos(ruta, progreso, salida, ventana):
    if not os.path.exists(ruta):
        messagebox.showerror("Error", "La carpeta no existe.")
        return

    # Crear subcarpetas
    for cat in categorias_texto + categorias_imagen:
        os.makedirs(os.path.join(ruta, cat), exist_ok=True)

    archivos = [f for f in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, f))]
    total = len(archivos)
    progreso["maximum"] = total
    progreso["value"] = 0
    salida.delete(1.0, "end")

    for i, archivo in enumerate(archivos, start=1):
        ruta_archivo = os.path.join(ruta, archivo)
        ext = os.path.splitext(archivo)[1].lower()
        if ext in [".txt", ".pdf", ".docx"]:
            categoria = clasificar_texto(ruta_archivo)
        elif ext in [".jpg", ".jpeg", ".png"]:
            categoria = clasificar_imagen(ruta_archivo)
        else:
            categoria = "otro"

        destino = os.path.join(ruta, categoria, archivo)
        shutil.move(ruta_archivo, destino)
        salida.insert("end", f"{archivo} → {categoria}\n")
        progreso["value"] = i
        ventana.update_idletasks()

    messagebox.showinfo("Completado", "¡Organización completada!")

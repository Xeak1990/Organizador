import os
import shutil
import threading
from tkinter import messagebox
from core.clasificador import (
    clasificar_texto,
    clasificar_imagen,
    categorias_texto_simple,
    categorias_imagen_simple
)

def organizar_archivos(ruta, progreso, salida, ventana, stop_event):
    if not os.path.exists(ruta):
        messagebox.showerror("Error", "La carpeta no existe.")
        return

    archivos = [f for f in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, f))]
    total = len(archivos)
    if total == 0:
        messagebox.showinfo("Info", "No hay archivos para organizar.")
        return

    # Crear solo carpetas necesarias
    todas_categorias = list(set(categorias_texto_simple + categorias_imagen_simple))
    for cat in todas_categorias:
        os.makedirs(os.path.join(ruta, cat), exist_ok=True)

    salida.delete("1.0", "end")
    salida.insert("end", f"🚀 Archivos encontrados: {total}\n\n")
    ventana.update()

    exitosos = 0
    errores = 0

    for i, archivo in enumerate(archivos, 1):
        if stop_event.is_set():
            salida.insert("end", "\n⏹ Proceso detenido por el usuario.\n")
            salida.see("end")
            break

        try:
            ruta_archivo = os.path.join(ruta, archivo)
            ext = os.path.splitext(archivo)[1].lower()

            # Clasificación
            if ext in [".txt", ".pdf", ".docx"]:
                categoria = clasificar_texto(ruta_archivo)
                tipo = "🤖"
            elif ext in [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"]:
                categoria = clasificar_imagen(ruta_archivo)
                tipo = "🖼️"
            else:
                categoria = "otro"
                tipo = "📦"

            salida.insert("end", f"📄 [{i}/{total}] {archivo} → {categoria}\n")
            ventana.update()

            # Mover archivo
            destino = os.path.join(ruta, categoria, archivo)
            if os.path.dirname(ruta_archivo) != os.path.dirname(destino):
                shutil.move(ruta_archivo, destino)
                exitosos += 1

            # Actualizar barra de progreso (0 a 1 para CTk)
            progreso.set(i / total)
            ventana.update_idletasks()

        except Exception as e:
            errores += 1
            salida.insert("end", f"   ❌ Error: {str(e)[:100]}...\n")
            continue

    if not stop_event.is_set():
        salida.insert("end", f"\n🎉 Proceso completado\nArchivos organizados: {exitosos}\nErrores: {errores}\n")
        messagebox.showinfo("Finalizado", f"Archivos organizados: {exitosos}\nErrores: {errores}")

import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, messagebox
from core.organizador import organizar_archivos

def seleccionar_carpeta(var):
    ruta = filedialog.askdirectory()
    if ruta:
        var.set(ruta)

def iniciar_interfaz():
    ventana = tk.Tk()
    ventana.title("Organizador de Archivos con IA")
    ventana.geometry("700x500")

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

    def ejecutar_organizacion():
        """Lanza la organización en un hilo aparte."""
        def tarea():
            try:
                salida.insert("end", "⏳ Iniciando organización...\n")
                salida.see("end")
                salida.update_idletasks()

                # Llama a tu función organizadora que ya use lazy loading
                organizar_archivos(carpeta_origen.get(), progreso, salida, ventana)

                salida.insert("end", "✅ Organización completada\n")
                salida.see("end")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        threading.Thread(target=tarea, daemon=True).start()

    tk.Button(
        ventana,
        text="Organizar Archivos",
        command=ejecutar_organizacion,
        bg="lightblue"
    ).pack(pady=10)

    ventana.mainloop()

import threading
import customtkinter as ctk
from core.organizador import organizar_archivos
from tkinter import filedialog

def seleccionar_carpeta(var):
    ruta = filedialog.askdirectory()
    if ruta:
        var.set(ruta)

def iniciar_proceso(carpeta_origen, progreso, salida, ventana, stop_event):
    hilo = threading.Thread(
        target=organizar_archivos,
        args=(carpeta_origen.get(), progreso, salida, ventana, stop_event),
        daemon=True
    )
    hilo.start()
    return hilo

def iniciar_interfaz():
    # Tema
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    ventana = ctk.CTk()
    ventana.title("Organizador de Archivos con IA")
    ventana.geometry("750x600")

    carpeta_origen = ctk.StringVar()
    stop_event = threading.Event()

    # Título
    titulo = ctk.CTkLabel(ventana, text="📂 Organizador de Archivos con IA", font=("Arial", 22, "bold"))
    titulo.pack(pady=20)

    # Selección de carpeta
    frame_carpeta = ctk.CTkFrame(ventana)
    frame_carpeta.pack(pady=10, padx=20, fill="x")

    entry_carpeta = ctk.CTkEntry(frame_carpeta, textvariable=carpeta_origen, width=400)
    entry_carpeta.pack(side="left", padx=10, pady=10)
    boton_carpeta = ctk.CTkButton(frame_carpeta, text="Seleccionar", command=lambda: seleccionar_carpeta(carpeta_origen))
    boton_carpeta.pack(side="left", padx=10)

    # Barra de progreso
    progreso = ctk.CTkProgressBar(ventana, width=500)
    progreso.set(0)
    progreso.pack(pady=20)

    # Caja de log
    salida = ctk.CTkTextbox(ventana, width=700, height=200)
    salida.pack(pady=20, padx=20)

    # Botones
    frame_botones = ctk.CTkFrame(ventana)
    frame_botones.pack(pady=10)
    boton_iniciar = ctk.CTkButton(frame_botones, text="🚀 Iniciar", fg_color="#1f6aa5",
                                  command=lambda: [stop_event.clear(), iniciar_proceso(carpeta_origen, progreso, salida, ventana, stop_event)])
    boton_iniciar.pack(side="left", padx=10)
    boton_detener = ctk.CTkButton(frame_botones, text="⏹ Detener", fg_color="#a51f1f",
                                  command=lambda: stop_event.set())
    boton_detener.pack(side="left", padx=10)

    ventana.mainloop()

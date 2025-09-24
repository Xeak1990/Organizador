import os
import re
from PIL import Image, ImageStat
import numpy as np

# Categorías simples
categorias_texto_simple = ["factura", "curriculum", "tarea", "articulo", "otro"]
categorias_imagen_simple = ["documento", "persona", "paisaje", "otro"]

# Variables globales para lazy load
_clasificador_texto = None
_clip_model = None
_clip_processor = None

# ===============================
# Carga de modelos
# ===============================
def get_text_classifier():
    global _clasificador_texto
    if _clasificador_texto is None:
        from transformers import pipeline
        _clasificador_texto = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
    return _clasificador_texto

def get_clip_models():
    global _clip_model, _clip_processor
    if _clip_model is None or _clip_processor is None:
        from transformers import CLIPProcessor, CLIPModel
        _clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        _clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return _clip_model, _clip_processor

# ===============================
# Clasificación de texto
# ===============================
def clasificar_texto(ruta):
    nombre_archivo = os.path.basename(ruta).lower()
    ext = os.path.splitext(ruta)[1].lower()
    texto = nombre_archivo

    if ext == ".txt":
        with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
            texto = f.read()[:1000]
    elif ext == ".pdf":
        try:
            import PyPDF2
            with open(ruta, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                texto = "".join([p.extract_text() or "" for p in reader.pages[:2]])
        except:
            pass
    elif ext == ".docx":
        try:
            import docx
            doc = docx.Document(ruta)
            texto = " ".join([p.text for p in doc.paragraphs[:20]])
        except:
            pass

    clasificador = get_text_classifier()
    categorias = categorias_texto_simple
    try:
        resultado = clasificador(texto, categorias, multi_label=False)
        return resultado["labels"][0]
    except:
        return "otro"

# ===============================
# Clasificación de imágenes
# ===============================
def clasificar_imagen(ruta):
    nombre_archivo = os.path.basename(ruta).lower()

    # Clasificación por nombre
    if any(pal in nombre_archivo for pal in ["captura", "pantalla", "screenshot"]):
        return "documento"
    if any(pal in nombre_archivo for pal in ["foto", "selfie", "persona", "retrato"]):
        return "persona"
    if any(pal in nombre_archivo for pal in ["paisaje", "vista", "naturaleza"]):
        return "paisaje"

    # Clasificación por IA CLIP
    try:
        clip_model, clip_processor = get_clip_models()
        image = Image.open(ruta).convert("RGB")
        inputs = clip_processor(text=categorias_imagen_simple, images=image, return_tensors="pt", padding=True)
        outputs = clip_model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)
        return categorias_imagen_simple[probs.argmax().item()]
    except:
        return "otro"

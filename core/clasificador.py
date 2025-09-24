import os
from PIL import Image

# Categorías
categorias_texto = ["factura", "curriculum", "tarea", "articulo", "otro"]
categorias_imagen = ["documento", "persona", "paisaje", "otro"]

# Variables globales (inicialmente vacías)
_clasificador_texto = None
_clip_model = None
_clip_processor = None


# === Funciones para cargar modelos bajo demanda ===
def get_text_classifier():
    global _clasificador_texto
    if _clasificador_texto is None:
        print("Cargando modelo de texto (esto puede tardar unos segundos)...")
        from transformers import pipeline
        _clasificador_texto = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
    return _clasificador_texto


def get_clip_models():
    global _clip_model, _clip_processor
    if _clip_model is None or _clip_processor is None:
        print("Cargando modelo de imágenes (esto puede tardar unos segundos)...")
        from transformers import CLIPProcessor, CLIPModel
        _clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        _clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return _clip_model, _clip_processor


# === Clasificación de texto ===
def clasificar_texto(ruta):
    try:
        ext = os.path.splitext(ruta)[1].lower()
        texto = ""
        if ext == ".txt":
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                texto = f.read()[:512]
        elif ext == ".pdf":
            import PyPDF2
            with open(ruta, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                texto = "".join([page.extract_text() for page in reader.pages[:2]])
        elif ext == ".docx":
            import docx
            doc = docx.Document(ruta)
            texto = "\n".join([p.text for p in doc.paragraphs[:20]])

        if texto.strip() == "":
            return "otro"

        clasificador = get_text_classifier()  # Lazy load aquí
        resultado = clasificador(texto, categorias_texto)
        return resultado["labels"][0]
    except Exception as e:
        print("Error en clasificar_texto:", e)
        return "otro"


# === Clasificación de imágenes ===
def clasificar_imagen(ruta):
    try:
        image = Image.open(ruta).convert("RGB")
        clip_model, clip_processor = get_clip_models()  # Lazy load aquí
        inputs = clip_processor(
            text=categorias_imagen,
            images=image,
            return_tensors="pt",
            padding=True
        )
        outputs = clip_model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)
        return categorias_imagen[probs.argmax().item()]
    except Exception as e:
        print("Error en clasificar_imagen:", e)
        return "otro"

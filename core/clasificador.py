import os
from transformers import pipeline, CLIPProcessor, CLIPModel
from PIL import Image
import torch

# Categorías
categorias_texto = ["factura", "curriculum", "tarea", "articulo", "otro"]
categorias_imagen = ["documento", "persona", "paisaje", "otro"]

# Modelos
clasificador_texto = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

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

        resultado = clasificador_texto(texto, categorias_texto)
        return resultado["labels"][0]
    except:
        return "otro"

def clasificar_imagen(ruta):
    try:
        image = Image.open(ruta).convert("RGB")
        inputs = clip_processor(text=categorias_imagen, images=image, return_tensors="pt", padding=True)
        outputs = clip_model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)
        return categorias_imagen[probs.argmax().item()]
    except:
        return "otro"

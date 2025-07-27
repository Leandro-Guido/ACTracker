from PIL import Image
import numpy as np
import face_recognition
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

def process_pil_image(image_pil, actor_name, metodo):
    """Processa uma imagem PIL e retorna os encodings com o nome do ator."""
    try:
        rgb = np.array(image_pil.convert("RGB"))
        boxes = face_recognition.face_locations(rgb, model=metodo)
        encodings = face_recognition.face_encodings(rgb, boxes)
        return [(encoding, actor_name) for encoding in encodings]
    except Exception as e:
        raise RuntimeError(f"Erro ao processar imagem: {e}")

def get_encodings_from_images(images, actor_name, metodo="hog"):
    """
    Recebe uma lista de objetos PIL.Image e o nome do ator.
    Retorna uma tupla: (lista de encodings, lista de nomes).
    """
    known_encodings = []
    known_names = []

    # Cria tarefas para processamento paralelo
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(process_pil_image, img, actor_name, metodo)
            for img in images
        ]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processando imagens"):
            result = future.result()
            for encoding, name in result:
                known_encodings.append(encoding)
                known_names.append(name)

    return known_encodings, known_names
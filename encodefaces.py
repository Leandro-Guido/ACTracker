from imutils import paths
import face_recognition
import pickle
import cv2
import os
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

ENCODINGS_FILE = "encodings.pickle"

def process_image(image_path, metodo):
    """Processa uma imagem e retorna os encodings e o nome do ator."""
    try:
        actor_name = os.path.basename(os.path.dirname(image_path))
        image = cv2.imread(image_path)
        if image is None:
            return []
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=metodo)
        encodings = face_recognition.face_encodings(rgb, boxes)
        return [(encoding, actor_name) for encoding in encodings]
    except Exception as e:
        raise RuntimeError(f"Erro ao processar imagem {image_path}: {e}")

def save_encodings_as_pkl(folder_name, metodo):

    image_paths = list(paths.list_images(folder_name))
    known_encodings = []
    known_names = []

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_image, path, metodo) for path in image_paths]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processando imagens"):
            result = future.result()
            for encoding, name in result:
                known_encodings.append(encoding)
                known_names.append(name)

    print("Salvando encodings...")
    data = {"encodings": known_encodings, "names": known_names}
    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)

from imutils import paths
import face_recognition
import pickle
import cv2
import os
from tqdm import tqdm
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed

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
        print(f"[ERRO] Falha ao processar {image_path}: {e}")
        return []

def main():
    # argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--encodings", type=str, required=True, help="path para salvar os encodings")
    ap.add_argument("-m", "--metodo",    type=str, default="hog", help="metodo de detecção facial `hog` ou `cnn`")
    args = vars(ap.parse_args())

    image_paths = list(paths.list_images("dataset"))
    known_encodings = []
    known_names = []

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_image, path, args["metodo"]) for path in image_paths]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processando imagens"):
            result = future.result()
            for encoding, name in result:
                known_encodings.append(encoding)
                known_names.append(name)

    print("Salvando encodings...")
    data = {"encodings": known_encodings, "names": known_names}
    with open(args["encodings"], "wb") as f:
        pickle.dump(data, f)

if __name__ == "__main__":
    main()
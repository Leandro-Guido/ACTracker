import face_recognition
import pickle
import cv2
import os
from tqdm import tqdm
import face_recognition

metodo = "hog" # "hog" ou "cnn"
dataset_path = "dataset"
encodings_path = "encodings.pickle"

def get_images_paths(dataset_path=dataset_path) -> str:
    dataset_path = os.path.join(os.getcwd(), dataset_path)
    folders = os.listdir(dataset_path)
    files = []

    for folder in folders:
        folder_path = os.path.join(dataset_path, folder)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                files.append(file_path)
    return files

print("[INFO] Carregando paths das imagens...")
images_paths = get_images_paths()

known_encodings = []
known_ids = []

# processando as imagens para obter os encodings de cada ator
for image_path in tqdm(images_paths, desc="[INFO] Processando imagens..."):
	id_ator = image_path.split(os.path.sep)[-2]
	image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
	face_locations = face_recognition.face_locations(image, model=metodo)
	encodings = face_recognition.face_encodings(image, face_locations)

	for encoding in encodings:
		known_encodings.append(encoding)
		known_ids.append(id_ator)

# salvando os encodings como pickle
print(f"[INFO] salvando encodings como {encodings_path}...")
data = {"encodings": known_encodings, "ids": known_ids}
print(data)

f = open(encodings_path, "wb")
f.write(pickle.dumps(data))
f.close()
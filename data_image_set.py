# ADAPTA OS DATA SETS PARA FUNCIONAR NA FUNCAO image_dataset_from_directory DO TF
#
# EXEMPLO DO TF:
# flower_photo/
#   daisy/
#   dandelion/
#   roses/
#   sunflowers/
#   tulips/
#
# No caso nosso é atores e subpastas com ids dos atores
# atores/
#   1/
#   2/
#   3/

import os
import shutil
import pandas as pd
from tqdm import tqdm

imdb = pd.read_csv("imdb.csv", encoding='latin1')
ids = pd.read_csv("ids.csv")

# criar nova estrutura de diretorios
for _, row in tqdm(imdb.iterrows(), total=len(imdb)):
    imageset_folder = "c:/Users/leand/OneDrive/Desktop/imdb_crop/imdb_crop/"
    nome_ator = str(int(ids[ids['name'] == row['name']]['id'].iloc[0]))
    caminho_img = imageset_folder + row["full_path"]

    pasta_ator = os.path.join("atores", nome_ator)
    os.makedirs(pasta_ator, exist_ok=True)

    nome_arquivo = os.path.basename(caminho_img)
    destino = os.path.join(pasta_ator, nome_arquivo)

    try:
        shutil.copy2(caminho_img, destino)
    except FileNotFoundError:
        print(f"imagem não encontrada: {caminho_img}")

print("imagens organizadas com sucesso.")

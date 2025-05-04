import os
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

API_KEY = "db1895eca7f93065adaac585e98eba99" # TMDB API KEY
BASE_URL = "https://api.themoviedb.org/3"

# quantos threads usar para download paralelo
MAX_WORKERS = 8

def tmdb_get(path, **params):
    """faz uma requisição GET para a API do TMDB e retorna o JSON da resposta"""
    url = f"{BASE_URL}{path}"
    params["api_key"] = API_KEY
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

def init_image_config():
    """pega a configuração de imagens do TMDB e retorna a url base e o tamanho da imagem"""
    cfg = tmdb_get("/configuration")
    base = cfg["images"]["secure_base_url"]
    sizes = cfg["images"]["profile_sizes"]
    return base, sizes[-1]

def sanitize_filename(name):
    """remove caracteres inválidos do nome do ator para criar um nome de arquivo seguro"""
    return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).strip()

def download_image(image_url, save_path):
    """faz download de uma imagem e salva na pasta dataset"""
    try:
        r = requests.get(image_url, stream=True, timeout=10)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        return True, save_path
    except Exception as e:
        return False, str(e)

def buscar_e_salvar_ator(actor_name):
    # buscar configuração de imagens
    image_base, image_size = init_image_config()

    # criar pasta dataset se não existir
    os.makedirs("dataset", exist_ok=True)

    # buscar informacoes do ator
    res = tmdb_get("/search/person", query=actor_name)
    if not res["results"]:
        print(f"ator '{actor_name}' não encontrado.")
        return

    actor = res["results"][0]
    actor_id = actor["id"]
    actor_name = sanitize_filename(actor["name"])

    # criar pasta do ator
    actor_folder = os.path.join("dataset", actor_name)
    os.makedirs(actor_folder, exist_ok=True)

    # buscar imagens do ator
    tasks = []
    imgs = tmdb_get(f"/person/{actor_id}/images").get("profiles", [])
    if not imgs:
        print(f"nenhuma imagem encontrada para o ator '{actor_name}'.")
        return

    for idx, img in enumerate(imgs, start=1):
        file_path = img["file_path"]
        url = f"{image_base}{image_size}{file_path}"
        save_as = os.path.join(actor_folder, f"{actor_name}_{idx}.jpg")
        tasks.append((url, save_as))

    # baixar imagens em paralelo
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(download_image, url, path) for url, path in tasks]
        for _ in tqdm(as_completed(futures), total=len(futures), desc="Baixando imagens"):
            pass

if __name__ == "__main__":
    buscar_e_salvar_ator("Rowan Atkinson")
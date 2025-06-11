"""
Funções para interagir com a API do TMDB e baixar imagens de atores.
"""
import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from io import BytesIO

API_KEY = "db1895eca7f93065adaac585e98eba99" # TMDB API KEY
BASE_URL = "https://api.themoviedb.org/3"

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

# para baixar imagem e converter para PIL
def download_to_pil(url):
    try:
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        return Image.open(BytesIO(r.content)).convert("RGB")
    except Exception as e:
        print(f"Erro ao baixar imagem: {e}")
        return None

def get_actor_pics(actor_name, threads=8):
    """
    Busca imagens do ator e retorna uma lista de objetos PIL.Image.
    """
    # buscar configuração de imagens
    image_base, image_size = init_image_config()

    # buscar informações do ator
    res = tmdb_get("/search/person", query=actor_name)
    if not res["results"]:
        print(f"Ator '{actor_name}' não encontrado.")
        return []

    actor = res["results"][0]
    actor_id = actor["id"]

    # buscar imagens do ator
    imgs = tmdb_get(f"/person/{actor_id}/images").get("profiles", [])
    if not imgs:
        print(f"Nenhuma imagem encontrada para o ator '{actor_name}'.")
        return []

    # construir lista de URLs
    urls = [f"{image_base}{image_size}{img['file_path']}" for img in imgs]

    # baixar imagens em paralelo
    images = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(download_to_pil, url) for url in urls]
        for future in tqdm(as_completed(futures), total=len(futures), desc="Baixando imagens"):
            img = future.result()
            if img is not None:
                images.append(img)

    return images

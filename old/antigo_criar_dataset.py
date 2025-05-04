import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── CONFIGURAÇÃO ───────────────────────────────────────────────────────────────

API_KEY = "db1895eca7f93065adaac585e98eba99"   # ⇨ coloque sua TMDB v3 API key aqui
BASE_URL = "https://api.themoviedb.org/3"

# Quantos atores baixar (os N primeiros do elenco)
TOP_N_ACTORS = 20
# Quantos threads usar para download paralelo
MAX_WORKERS = 8

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def tmdb_get(path, **params):
    url = f"{BASE_URL}{path}"
    params["api_key"] = API_KEY
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

def init_image_config():
    cfg = tmdb_get("/configuration")
    base = cfg["images"]["secure_base_url"]
    sizes = cfg["images"]["profile_sizes"]
    # vamos usar sempre a maior resolução disponível:
    return base, sizes[-1]

def sanitize_filename(name):
    return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).strip()

def download_image(image_url, save_path):
    """Faz download de uma imagem e salva em disco."""
    try:
        r = requests.get(image_url, stream=True, timeout=10)
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        return True, save_path
    except Exception as e:
        return False, str(e)

# ─── FLUXO PRINCIPAL ───────────────────────────────────────────────────────────

def fetch_and_save_actors(movie_name):
    # 1) buscar configuração de imagens
    image_base, image_size = init_image_config()

    # 2) buscar filme
    res = tmdb_get("/search/movie", query=movie_name)
    if not res["results"]:
        print(f"❌ Filme '{movie_name}' não encontrado.")
        return

    movie = res["results"][0]
    movie_id = movie["id"]
    title = sanitize_filename(movie["title"])
    print(f"▶️ Baixando atores de: {title} (ID {movie_id})")

    # 3) criar pasta principal
    root_folder = f"atores_{title}"
    os.makedirs(root_folder, exist_ok=True)

    # 4) buscar elenco
    credits = tmdb_get(f"/movie/{movie_id}/credits")
    cast = credits.get("cast", [])[:TOP_N_ACTORS]
    print(f"ℹ️ Serão baixados os {len(cast)} primeiros atores do elenco.")

    # 5) preparar lista de tarefas (actor_id, nome, lista de URLs)
    tasks = []
    for person in cast:
        pid = person["id"]
        name = sanitize_filename(person["name"])
        folder = os.path.join(root_folder, name)
        os.makedirs(folder, exist_ok=True)

        imgs = tmdb_get(f"/person/{pid}/images").get("profiles", [])
        for idx, img in enumerate(imgs, start=1):
            file_path = img["file_path"]
            url = f"{image_base}{image_size}{file_path}"
            save_as = os.path.join(folder, f"{name}_{idx}.jpg")
            tasks.append((url, save_as))

    # 6) baixar imagens em paralelo
    print(f"🔄 Iniciando download paralelo com {MAX_WORKERS} threads...")
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_task = {executor.submit(download_image, url, out): (url, out)
                          for url, out in tasks}

        for future in as_completed(future_to_task):
            url, out = future_to_task[future]
            success, info = future.result()
            if success:
                print(f"✅ {os.path.basename(out)} salvo.")
            else:
                print(f"❌ Erro em {os.path.basename(out)}: {info}")

    print("🎉 Download concluído.")

if __name__ == "__main__":
    fetch_and_save_actors("Mr. Bean - O Filme")
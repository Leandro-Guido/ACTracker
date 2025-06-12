import requests
import time

ATOR = "Morgan Freeman"
METODO = "hog"
DISPLAY = 0
RESIZE_WIDTH = 300
THRESHOLD = 0.55
FRAME_SKIP = 20
URL = "http://localhost:5000/tempo_tela"

def testar_escalabilidade_forte():
    print("\n🔬 Escalabilidade Forte:")
    filme = "Cut 32 Um Sonho de Liberdade"
    for threads in [1, 2, 4, 8]:
        print(f"\n⏱ Threads: {threads}")
        payload = {
            "ator": ATOR,
            "filme": filme,
            "threads": threads,
            "metodo": METODO,
            "display": DISPLAY,
            "resize_width": RESIZE_WIDTH,
            "threshold": THRESHOLD,
            "frame_skip": FRAME_SKIP
        }
        inicio = time.time()
        resposta = requests.post(URL, json=payload).json()
        fim = time.time()
        print(f"Resposta: {resposta}")
        print(f"Tempo de execução: {fim - inicio:.2f} segundos")

def testar_escalabilidade_fraca():
    print("\n🔬 Escalabilidade Fraca:")
    cortes = {
        1: "Cut 4 Um Sonho de Liberdade",
        2: "Cut 8 Um Sonho de Liberdade",
        4: "Cut 16 Um Sonho de Liberdade",
        8: "Cut 32 Um Sonho de Liberdade"
    }
    for threads, filme in cortes.items():
        print(f"\n⏱ Threads: {threads}, Filme: {filme}")
        payload = {
            "ator": ATOR,
            "filme": filme,
            "threads": threads,
            "metodo": METODO,
            "display": DISPLAY,
            "resize_width": RESIZE_WIDTH,
            "threshold": THRESHOLD,
            "frame_skip": FRAME_SKIP
        }
        inicio = time.time()
        resposta = requests.post(URL, json=payload).json()
        fim = time.time()
        print(f"Resposta: {resposta}")
        print(f"Tempo de execução: {fim - inicio:.2f} segundos")

if __name__ == "__main__":
    testar_escalabilidade_forte()
    testar_escalabilidade_fraca()
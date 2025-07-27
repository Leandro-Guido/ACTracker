import requests
import time
import csv

# Configurações globais
ATOR = "Tim Robbins"
METODO = "hog"
DISPLAY = 1
RESIZE_WIDTH = 300
THRESHOLD = 0.55
URL = "http://localhost:5000/tempo_tela"
CSV_FILENAME = "resultados_benchmark.csv"

# Salva os resultados em CSV
def salvar_csv(resultados):
    with open(CSV_FILENAME, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "tipo", "filme", "threads", "frame_skip",
            "tempo_execucao", "tempo_em_tela", "duracao_total"
        ])
        writer.writeheader()
        for linha in resultados:
            writer.writerow(linha)

# Função genérica de benchmark
def executar_benchmark(tipo, filme, threads, frame_skip):
    payload = {
        "ator": ATOR,
        "filme": filme,
        "threads": threads,
        "metodo": METODO,
        "display": DISPLAY,
        "resize_width": RESIZE_WIDTH,
        "threshold": THRESHOLD,
        "frame_skip": frame_skip
    }
    inicio = time.time()
    resposta = requests.post(URL, json=payload).json()
    fim = time.time()
    tempo_execucao = round(fim - inicio, 2)

    print(f"[{tipo}] Threads: {threads}, Frame Skip: {frame_skip}, Filme: {filme}")
    print(f"Tempo Execução: {tempo_execucao}s")

    return {
        "tipo": tipo,
        "filme": filme,
        "threads": threads,
        "frame_skip": frame_skip,
        "tempo_execucao": tempo_execucao,
        "tempo_em_tela": resposta.get("tempo_em_tela_segundos", -1),
        "duracao_total": resposta.get("duracao_total_segundos", -1)
    }

# Escalabilidade forte (variando threads)
def testar_escalabilidade_forte_threads():
    print("\n[Escalabilidade Forte - Threads]")
    resultados = []
    filme = "Cut 48 Um Sonho de Liberdade"
    frame_skip = 60
    for threads in [1, 2, 4, 8, 12]:
        resultado = executar_benchmark("forte_threads", filme, threads, frame_skip)
        resultados.append(resultado)
    return resultados

# Escalabilidade forte (variando frame_skip)
def testar_escalabilidade_forte_frame_skip():
    print("\n[Escalabilidade Forte - Frame Skip]")
    resultados = []
    filme = "Cut 48 Um Sonho de Liberdade"
    threads = 12
    for frame_skip in [1, 2, 10, 20, 40, 90]:
        resultado = executar_benchmark("forte_frame_skip", filme, threads, frame_skip)
        resultados.append(resultado)
    return resultados

# Escalabilidade fraca (aumentando corte e threads)
def testar_escalabilidade_fraca():
    print("\n[Escalabilidade Fraca]")
    resultados = []
    cortes = {
        1: "Cut 4 Um Sonho de Liberdade",
        2: "Cut 8 Um Sonho de Liberdade",
        4: "Cut 16 Um Sonho de Liberdade",
        8: "Cut 32 Um Sonho de Liberdade",
        12: "Cut 48 Um Sonho de Liberdade"
    }
    frame_skip = 60
    for threads, filme in cortes.items():
        resultado = executar_benchmark("fraca", filme, threads, frame_skip)
        resultados.append(resultado)
    return resultados

# Execução principal
if __name__ == "__main__":
    todos_os_resultados = []
    todos_os_resultados.extend(testar_escalabilidade_forte_threads())
    todos_os_resultados.extend(testar_escalabilidade_forte_frame_skip())
    todos_os_resultados.extend(testar_escalabilidade_fraca())
    salvar_csv(todos_os_resultados)
    print(f"\nTodos os resultados foram salvos em {CSV_FILENAME}")

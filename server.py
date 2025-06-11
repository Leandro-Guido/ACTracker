from flask import Flask, request, jsonify
import tmdb
import encodefaces
import recognize_faces
import cv2
import os
import multiprocessing

# Configuração do Ngrok
# ngrok http 5000

app = Flask(__name__)

@app.route('/tempo_tela', methods=['POST'])
def tempo_tela():
    data = request.json
    ator = data.get("ator")
    filme = data.get("filme")
    metodo = data.get("metodo", "hog")
    threads = data.get("threads", 1)
    display = data.get("display", 0)
    resize_width = data.get("resize_width", 300)
    threshold = data.get("threshold", 0.55)
    frame_skip = data.get("frame_skip", 20)

    if not ator or not filme:
        return jsonify({"erro": "Parâmetros 'ator' e 'filme' são obrigatórios."}), 400

    path_filme = f"filmes/{filme}.mp4"
    if not os.path.exists(path_filme):
        return jsonify({"erro": f"O filme '{filme}.mp4' não foi encontrado em 'filmes/'"}), 404

    try:
        # Corrige erro de multiprocessing no Windows
        multiprocessing.set_start_method("spawn", force=True)

        # Baixar imagens do ator (em memória)
        actor_pics = tmdb.get_actor_pics(ator, threads=12)
        if not actor_pics:
            return jsonify({"erro": f"Nenhuma imagem encontrada para o ator '{ator}'"}), 404

        # Obter encodings em memória
        encodings, names = encodefaces.get_encodings_from_images(actor_pics, ator, metodo=metodo)

        # Abrir vídeo
        vs = cv2.VideoCapture(path_filme)
        if not vs.isOpened():
            return jsonify({"erro": f"Erro ao abrir o vídeo '{filme}.mp4'"}), 500

        tempo_tela_seg = recognize_faces.encontrar_tempo_de_tela_ator(
            ator=ator,
            all_encodings=encodings,
            all_names=names,
            path_filme=path_filme,
            metodo=metodo,
            resize_width=resize_width,
            threshold=threshold,
            frame_skip=frame_skip,
            display=display,
            threads=threads
        )

        duracao_total = vs.get(cv2.CAP_PROP_FRAME_COUNT) / vs.get(cv2.CAP_PROP_FPS)
        vs.release()

        print(f"Tempo total em tela do ator '{ator}': {tempo_tela_seg:.2f} segundos.")
        print(f"Tempo do filme: {vs.get(cv2.CAP_PROP_FRAME_COUNT) / vs.get(cv2.CAP_PROP_FPS):.2f} segundos.")

        return jsonify({
            "ator": ator,
            "filme": filme,
            "tempo_em_tela_segundos": round(tempo_tela_seg, 2),
            "duracao_total_segundos": round(duracao_total, 2)
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn", force=True)
    app.run(debug=True, host="0.0.0.0", port=5000)

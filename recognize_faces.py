import face_recognition
import imutils
import pickle
import cv2
import numpy as np
import argparse
from tqdm import tqdm

def encontrar_tempo_de_tela_ator(ator, all_encodings, all_names, vs:cv2.VideoCapture, metodo, resize_width, threshold, frame_skip, display):

    # progresso
    total_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT) / frame_skip)
    pbar = tqdm(total=total_frames, desc="Processando vídeo", unit="frame")
    tqdm.write(f"Total de frames no vídeo: {total_frames}")

    frame_number = 0
    frame_actor_count = 0

    # loop sobre os frames do vídeo
    while True:
        vs.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = vs.read()
        if not ret:
            break

        # otimização: ignora frames muito escuros
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if cv2.mean(gray)[0] < 20:
            frame_number += frame_skip
            pbar.update(1)
            continue

        # redimensiona frame para acelerar o processamento
        frame_resized = imutils.resize(frame, width=resize_width)
        rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        scale = frame.shape[1] / float(frame_resized.shape[1])

        # detecta rostos
        boxes = face_recognition.face_locations(rgb, model=metodo)

        if boxes:
            # calcula os encodings de todos os rostos encontrados
            frame_encodings = face_recognition.face_encodings(rgb, boxes, model="small")
            actor_names = []

            for encoding in frame_encodings:
                distances = face_recognition.face_distance(all_encodings, encoding) # compara com os encodings conhecidos
                actor_name = "Unknown"
                if len(distances) > 0:
                    min_dist = np.min(distances)
                    if min_dist < threshold:
                        index = np.argmin(distances)
                        actor_name = all_names[index]
                if actor_name == ator:
                    frame_actor_count += 1
                actor_names.append(actor_name)

            # desenha os nomes
            if display > 0:
                for ((top, right, bottom, left), actor_name) in zip(boxes, actor_names):
                    top = int(top * scale)
                    right = int(right * scale)
                    bottom = int(bottom * scale)
                    left = int(left * scale)
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    y = top - 15 if top - 15 > 15 else top + 15
                    cv2.putText(frame, actor_name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        if display > 0:
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

        pbar.update(1)
        frame_number += frame_skip

    # finalização
    cv2.destroyAllWindows()
    print(f"Ator '{ator}' apareceu em {frame_actor_count} frames.")

    fps = vs.get(cv2.CAP_PROP_FPS)
    return (frame_actor_count / fps) * frame_skip

def main():
    # argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--encodings",    type=str,   required=True,  help="path para carregar os encodings")
    ap.add_argument("-i", "--input",        type=str,   required=True,  help="path para o video de entrada")
    ap.add_argument("-a", "--actor",        type=str,   required=True,  help="nome do ator a ser reconhecido no video")
    ap.add_argument("-d", "--display",      type=int,   default=1,      help="exibir video (0 ou 1)")
    ap.add_argument("-m", "--metodo",       type=str,   default="hog",  help="metodo de detecção facial `hog` ou `cnn`")
    ap.add_argument("-r", "--resize_width", type=int,   default=500,    help="largura para redimensionar o video")
    ap.add_argument("-t", "--threshold",    type=float, default=0.55,   help="distancia máxima aceitavel para correspondencia")
    ap.add_argument("-f", "--frame_skip",   type=int,   default=1,      help="numero de frames a pular\n exemplo: frame_skip = 20 então pula 19, processa 1")
    args = vars(ap.parse_args())

    # carrega os encodings
    with open(args["encodings"], "rb") as f:
        data = pickle.load(f)

    # abrir video
    vs = cv2.VideoCapture(args["input"])
    if not vs.isOpened():
        raise ValueError(f"Erro ao abrir o video: {args['input']}")
    
    tempo_tela_seg = encontrar_tempo_de_tela_ator(
        ator=args["actor"],
        all_encodings=data["encodings"],
        all_names=data["names"],
        vs=vs,
        metodo=args["metodo"],
        resize_width=args["resize_width"],
        threshold=args["threshold"],
        frame_skip=args["frame_skip"],
        display=args["display"]
    )

    print(f"Tempo total em tela do ator '{args['actor']}': {tempo_tela_seg:.2f} segundos.")
    print(f"Tempo do filme: {vs.get(cv2.CAP_PROP_FRAME_COUNT) / vs.get(cv2.CAP_PROP_FPS):.2f} segundos.")
    
    # libera o video
    vs.release()


if __name__ == "__main__":
    main()
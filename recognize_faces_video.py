import face_recognition
import imutils
import pickle
import cv2
import numpy as np
import argparse

def main(): 
    # argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--encodings", type=str, required=True, help="path para carregar os encodings")
    ap.add_argument("-i", "--input", type=str, required=True, help="path para o vídeo de entrada")
    ap.add_argument("-d", "--display", type=int, default=1, help="exibir vídeo (0 ou 1)")
    ap.add_argument("-m", "--metodo", type=str, default="hog", help="metodo de detecção facial `hog` ou `cnn`")
    ap.add_argument("-r", "--resize_width", type=int, default=500, help="largura para redimensionar o vídeo")
    ap.add_argument("-t", "--threshold", type=float, default=0.55, help="distância máxima aceitável para correspondência")
    ap.add_argument("-f", "--frame_skip", type=int, default=20, help="número de frames a pular\n exemplo: frame_skip = 20 então pula 19, processa 1")
    args = vars(ap.parse_args())

    # carrega os encodings
    with open(args["encodings"], "rb") as f:
        data = pickle.load(f)

    # carrega o vídeo
    vs = cv2.VideoCapture(args["input"])

    frame_skip = 20
    frame_count = 0

    display = args["display"]
    metodo = args["metodo"]
    resize_width = args["resize_width"]
    threshold = args["threshold"]

    # loop sobre os frames do vídeo
    while True:
        ret, frame = vs.read()
        if not ret:
            break

        # otimização: pula frames para acelerar o processamento
        frame_count += 1
        if frame_count % frame_skip != 0:
            continue  # pula este frame

        # otimização: ignora frames muito escuros
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = cv2.mean(gray)[0]
        if mean_brightness < 20:
            continue  # ignora o frame

        # redimensiona frame para acelerar o processamento
        frame_resized = imutils.resize(frame, width=resize_width)
        rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        scale = frame.shape[1] / float(frame_resized.shape[1])

        boxes = face_recognition.face_locations(rgb, model=metodo)

        if boxes:
            encodings = face_recognition.face_encodings(rgb, boxes, model="small")
            actor_names = []

            for encoding in encodings:
                distances = face_recognition.face_distance(data["encodings"], encoding)
                actor_name = "Unknown"
                if len(distances) > 0:
                    min_dist = np.min(distances)
                    if min_dist < threshold:
                        index = np.argmin(distances)
                        actor_name = data["names"][index]

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

    # finalização
    vs.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
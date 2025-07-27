import face_recognition
import imutils
import pickle
import cv2
import numpy as np
import argparse
import multiprocessing
import os


def process_video_segment(proc_id, args, start_frame, end_frame):
    # Carrega os encodings
    with open(args["encodings"], "rb") as f:
        data = pickle.load(f)

    # Abre o vídeo novamente
    vs = cv2.VideoCapture(args["input"])
    vs.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    metodo = args["metodo"]
    resize_width = args["resize_width"]
    threshold = args["threshold"]
    display = args["display"]
    frame_skip = args["frame_skip"]

    frame_count = start_frame
    window_name = f"Thread-{proc_id}"

    while frame_count <= end_frame:
        ret, frame = vs.read()
        if not ret:
            break

        frame_count += 1
        if frame_skip > 1 and frame_count % frame_skip != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_brightness = cv2.mean(gray)[0]
        if mean_brightness < 20:
            continue

        frame_resized = imutils.resize(frame, width=resize_width)
        rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        scale = frame.shape[1] / float(frame_resized.shape[1])

        boxes = face_recognition.face_locations(rgb, model=metodo)
        actor_names = []

        if boxes:
            encodings = face_recognition.face_encodings(rgb, boxes, model="small")
            for encoding in encodings:
                distances = face_recognition.face_distance(data["encodings"], encoding)
                actor_name = "Unknown"
                if len(distances) > 0:
                    min_dist = np.min(distances)
                    if min_dist < threshold:
                        index = np.argmin(distances)
                        actor_name = data["names"][index]
                actor_names.append(actor_name)

        if display > 0:
            for ((top, right, bottom, left), actor_name) in zip(boxes, actor_names):
                top = int(top * scale)
                right = int(right * scale)
                bottom = int(bottom * scale)
                left = int(left * scale)
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, actor_name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    vs.release()
    cv2.destroyWindow(window_name)

def main():
    # Argumentos
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", "--encodings", type=str, required=True, help="path para os encodings")
    ap.add_argument("-i", "--input", type=str, required=True, help="path do vídeo de entrada")
    ap.add_argument("-d", "--display", type=int, default=1, help="mostrar vídeo (1 ou 0)")
    ap.add_argument("-m", "--metodo", type=str, default="hog", help="hog ou cnn")
    ap.add_argument("-r", "--resize_width", type=int, default=500, help="largura para redimensionamento")
    ap.add_argument("-t", "--threshold", type=float, default=0.55, help="limiar de distância")
    ap.add_argument("-f", "--frame_skip", type=int, default=20, help="frames a pular")
    ap.add_argument("-n", "--threads", type=int, required=True, help="número de processos")
    args = vars(ap.parse_args())

    num_threads = args["threads"]

    # Verifica número total de frames
    vs = cv2.VideoCapture(args["input"])
    total_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
    vs.release()

    # Calcula os intervalos de frames para cada processo
    frames_per_thread = total_frames // num_threads
    processes = []

    for i in range(num_threads):
        start_frame = i * frames_per_thread
        end_frame = (i + 1) * frames_per_thread - 1 if i != num_threads - 1 else total_frames - 1
        p = multiprocessing.Process(target=process_video_segment, args=(i, args, start_frame, end_frame))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print("[INFO] Todos os processos terminaram.")


if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')  # Windows/Linux compatível
    main()

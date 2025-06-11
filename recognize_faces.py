import face_recognition
import imutils
import cv2
import numpy as np
import multiprocessing

def encontrar_tempo_de_tela_ator(ator, all_encodings, all_names, path_filme, metodo, resize_width, threshold, frame_skip, display, threads):

    # Verifica número total de frames
    vs = cv2.VideoCapture(path_filme)
    total_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
    vs.release()

    # Calcula os intervalos de frames para cada processo
    frames_per_thread = total_frames // threads
    processes = []

    queue = multiprocessing.Queue()

    for i in range(threads):
        start_frame = i * frames_per_thread
        end_frame = (i + 1) * frames_per_thread - 1 if i != threads - 1 else total_frames - 1
        p = multiprocessing.Process(target=process_video_segment, args=(i, ator, all_encodings, all_names, path_filme, metodo, resize_width, threshold, frame_skip, display, start_frame, end_frame, queue))
        print(f"[INFO] Iniciando processo {i} para o ator '{ator}' do frame {start_frame} ao {end_frame}.")
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    # Coletar resultados da fila
    tempos = []
    while not queue.empty():
        tempos.append(queue.get())

    print("[INFO] Todos os processos terminaram.")

    return sum(tempos)


def process_video_segment(proc_id, ator, all_encodings, all_names, path_filme, metodo, resize_width, threshold, frame_skip, display, start_frame, end_frame, queue):

    # Abre o vídeo novamente
    vs = cv2.VideoCapture(path_filme)
    vs.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frame_actor_count = 0

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

        boxes = face_recognition.face_locations(rgb, model=metodo)
        actor_names = []

        if boxes:
            encodings = face_recognition.face_encodings(rgb, boxes, model="small")
            for encoding in encodings:
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

        if display > 0:
            for ((top, right, bottom, left), actor_name) in zip(boxes, actor_names):
                top = int(top)
                right = int(right)
                bottom = int(bottom)
                left = int(left)
                cv2.rectangle(frame_resized, (left, top), (right, bottom), (0, 255, 0), 2)
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame_resized, actor_name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

            cv2.imshow(window_name, frame_resized)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    # finalização
    fps = vs.get(cv2.CAP_PROP_FPS)
    vs.release()
    cv2.destroyAllWindows()
    print(f"Ator '{ator}' apareceu em {frame_actor_count} frames.")

    tempo_seg = (frame_actor_count / fps) * frame_skip

    queue.put(tempo_seg)
import tmdb
import argparse
import encodefaces
import multiprocessing
import recognize_faces
import cv2

def main():
    ap = argparse.ArgumentParser(description="Cria um dataset de atores a partir do TMDB.")
    ap.add_argument("-a", "--actor",        type=str,   required=True,  help="nome do ator a ser buscado")
    ap.add_argument("-f", "--filme",        type=str,   required=True,  help='nome do filme')
    ap.add_argument("-m", "--metodo",       type=str,   default="hog",  help="metodo de detecção facial `hog` ou `cnn`")
    ap.add_argument("-d", "--display",      type=int,   default=0,      help="exibir video (0 ou 1) só funciona com 1 thread")
    ap.add_argument("-r", "--resize_width", type=int,   default=300,    help="largura para redimensionar o video")
    ap.add_argument("-t", "--threshold",    type=float, default=0.55,   help="distancia máxima aceitavel para correspondencia")
    ap.add_argument("-s", "--frame_skip",   type=int,   default=20,      help="numero de frames a pular\n exemplo: frame_skip = 20 então pula 19, processa 1")
    ap.add_argument("-n", "--threads",      type=int,   required=True,  help="número de processos")
    args = vars(ap.parse_args())

    path_filme = f"filmes/{args['filme']}.mp4"

    # BAIXAR AS FOTOS DO ATOR
    actor_pics = tmdb.get_actor_pics(args["actor"], threads=12) # threads fixa em 12 pq não é onde queremos testar o paralelismo

    # FOTOS DO ATOR COMO ENCODINGS
    encodings, names= encodefaces.get_encodings_from_images(actor_pics,  args["actor"], metodo=args["metodo"])

    # RECONHECIMENTO DOS ATORES

    # abrir video
    vs = cv2.VideoCapture(path_filme)
    if not vs.isOpened():
        raise ValueError(f"Erro ao abrir o video: {args['filme']}.mp4")

    tempo_tela_seg = recognize_faces.encontrar_tempo_de_tela_ator(
        ator=args["actor"],
        all_encodings=encodings,
        all_names=names,
        path_filme=path_filme,
        metodo=args["metodo"],
        resize_width=args["resize_width"],
        threshold=args["threshold"],
        frame_skip=args["frame_skip"],
        display=args["display"],
        threads=args["threads"]
    )

    print(f"Tempo total em tela do ator '{args['actor']}': {tempo_tela_seg:.2f} segundos.")
    print(f"Tempo do filme: {vs.get(cv2.CAP_PROP_FRAME_COUNT) / vs.get(cv2.CAP_PROP_FPS):.2f} segundos.")
    
    # libera o video
    vs.release()

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn')
    main()
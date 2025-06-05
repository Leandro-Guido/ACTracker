import tmdb
import argparse
import encodefaces
import cortar_filme
import recognize_faces
import pickle
import cv2

# pasta onde as fotos dos atores serão salvas
FOLDER_IMAGES = "dataset"

# arquivo onde os encodings serão salvos
ENCODINGS_FILE = "encodings.pickle"

def main():
    ap = argparse.ArgumentParser(description="Cria um dataset de atores a partir do TMDB.")
    ap.add_argument("-a", "--actor",        type=str,   required=True,  help="nome do ator a ser buscado")
    ap.add_argument("-f", "--filme",        type=str,   required=True,  help='nome do filme')
    ap.add_argument("-m", "--metodo",       type=str,   default="hog",  help="metodo de detecção facial `hog` ou `cnn`")
    ap.add_argument("-w", "--threads",      type=int,   default=1,      help='quantidade de threads')
    ap.add_argument("-d", "--display",      type=int,   default=0,      help="exibir video (0 ou 1) só funciona com 1 thread")
    ap.add_argument("-r", "--resize_width", type=int,   default=500,    help="largura para redimensionar o video")
    ap.add_argument("-t", "--threshold",    type=float, default=0.55,   help="distancia máxima aceitavel para correspondencia")
    ap.add_argument("-s", "--frame_skip",   type=int,   default=1,      help="numero de frames a pular\n exemplo: frame_skip = 20 então pula 19, processa 1")
    args = vars(ap.parse_args())

    path_filme = f"filmes/{args['filme']}.mp4"
    cortes = f"cortes/{args['filme']}"

    # BAIXAR AS FOTOS DO ATOR
    tmdb.download_actor_pics(args["actor"], FOLDER_IMAGES, threads=12) # threads fixa em 12 pq não é onde queremos testar o paralelismo

    # SALVAR AS FOTOS DO ATOR COMO ENCODINGS
    encodefaces.save_encodings_as_pkl(FOLDER_IMAGES, metodo=args["metodo"])

    # CORTAR O FILME EM PARTES (PARA PARALELISMO)
    cortar_filme.cortar_em_partes( input_file=path_filme, partes=args["threads"])

    # RECONHECIMENTO DOS ATORES

    # carrega os encodings
    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)

    # abrir video
    vs = cv2.VideoCapture(path_filme)
    if not vs.isOpened():
        raise ValueError(f"Erro ao abrir o video: {args['filme']}.mp4")
    input("Achou o filme")

    tempo_tela_seg = recognize_faces.encontrar_tempo_de_tela_ator(
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
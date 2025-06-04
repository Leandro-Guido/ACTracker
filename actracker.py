import tmdb
import argparse
import encodefaces

# pasta onde as fotos dos atores serão salvas
FOLDER_IMAGES = "dataset"

def main():

    ap = argparse.ArgumentParser(description="Cria um dataset de atores a partir do TMDB.")
    ap.add_argument("-a", "--actor",  type=str, required=True, help="nome do ator a ser buscado")
    ap.add_argument("-m", "--metodo", type=str, default="hog", help="metodo de detecção facial `hog` ou `cnn`")
    args = vars(ap.parse_args())

    tmdb.download_actor_pics(args["actor"], FOLDER_IMAGES, threads=12)
    encodefaces.save_encodings_as_pkl(FOLDER_IMAGES, metodo=args["metodo"])

if __name__ == "__main__":
    main()
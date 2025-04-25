from scipy.io import loadmat
import pandas as pd
import numpy as np
import csv

print("\nCONVERTENDO IMDB.MAT PARA IMDB.CSV...")

# carregar como dict
mat_data = loadmat('imdb.mat')

# os ultimos 2 indices tem o id de cada ator
keys = list(mat_data['imdb'].dtype.names)[0:7]

imdb_data = mat_data['imdb'][0][0]

qnt_linhas_csv = len(imdb_data[0][0])

face_score_minimo = 5

with open("imdb.csv", mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames = keys)
    writer.writeheader()
    for i_row in range(qnt_linhas_csv):
        data_row = dict()
        for k in range(len(keys)):
            if type(imdb_data[k][0][i_row]) == np.ndarray:
                data_row[keys[k]] = imdb_data[k][0][i_row][0]
            else:
                data_row[keys[k]] = imdb_data[k][0][i_row]
        if(float(imdb_data[6][0][i_row] >= face_score_minimo and np.isnan(float(imdb_data[7][0][i_row])))):
            writer.writerow(data_row)

print("CRIANDO CSV COM RELAÇÃO ID, NOME...")

relacao = {'name': []}
for i_row in range(qnt_linhas_csv):
    data_row = dict()
    for r in relacao:
        if r == 'name':
            relacao['name'].append(imdb_data[4][0][i_row][0])
relacao = pd.DataFrame(relacao).drop_duplicates()
relacao = relacao.sort_index(ignore_index=True)
relacao.to_csv("ids.csv", index_label="id")

print("PRONTO.")
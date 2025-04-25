import pandas as pd

csv_completo = pd.read_csv('imdb.csv', encoding='latin1')

csv_reduzido = csv_completo[csv_completo['full_path'].str.startswith('00')]
csv_completo = None

csv_reduzido.to_csv('csv_reduzido.csv', index=False)
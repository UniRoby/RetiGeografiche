import pandas as pd

# Carica i due dataset CSV
df_tuo_file = pd.read_csv('commenti_dataset_r.csv')
df_righe_selezionate = pd.read_csv('righe_selezionate.csv')

# Concatena i due DataFrame
df_concatenato = pd.concat([df_tuo_file, df_righe_selezionate], ignore_index=True)

# Salva il DataFrame concatenato nel file CSV originale
df_concatenato.to_csv('commenti_dataset_r.csv', index=False)

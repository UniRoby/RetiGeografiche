import pandas as pd

# Carica il dataset CSV
df = pd.read_csv('commenti_dataset_r.csv')

# Definisci i valori da filtrare
social_da_cancellare =  'YouTube'
giornale_da_cancellare = 'La Repubblica'
titolo_da_cancellare = 'Strage di Cutro'

# Trova le righe da selezionare
selected_rows = df[(df['social'] == social_da_cancellare) & (df['giornale'] == giornale_da_cancellare) & (df['titolo'] == titolo_da_cancellare)]

# Stampa il nuovo DataFrame con le righe selezionate
print(selected_rows)

# Salva il DataFrame in un nuovo file CSV
selected_rows.to_csv('righe_selezionate.csv', index=False)

import pandas as pd

# Carica il dataset CSV
df = pd.read_csv('nomecsv')

# Definisci i valori da filtrare
social_da_cancellare = input("Social da cancellare: ")
giornale_da_cancellare = input("Giornale da cancellare: ")
titolo_da_cancellare = input("Titolo da cancellare: ")


# Filtra il DataFrame per rimuovere le righe con i valori specificati
df = df[~((df['social'] == social_da_cancellare) & (df['giornale'] == giornale_da_cancellare) & (df['titolo'] == titolo_da_cancellare))]

# Sovrascrivi il file CSV originale
df.to_csv('nomecsv', index=False)


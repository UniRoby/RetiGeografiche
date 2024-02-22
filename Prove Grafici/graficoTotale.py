import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

# Leggi il file CSV
df = pd.read_csv('/Users/roby/PycharmProjects/RetiGeografiche/commenti_dataset_r.csv')

# Filtra i commenti positivi, negativi e di hate speech
commenti_positivi = df[df['sentiment'] == 'positivo']
commenti_negativi = df[df['sentiment'] == 'negativo']
commenti_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]

# Calcola il numero totale di commenti per ciascuna categoria
total_positivi = len(commenti_positivi)
total_negativi = len(commenti_negativi)
total_hate_speech = len(commenti_hate_speech)

categories = ['Positivi', 'Negativi', 'Hate Speech']
totals = [total_positivi, total_negativi, total_hate_speech]

plt.figure(figsize=(10, 6))
plt.bar(categories, totals, color=['green', 'orange', 'red'])
plt.title('Numero Totale di commenti per categoria',fontweight='bold')
plt.xlabel('Categoria', fontweight='bold')
plt.ylabel('Numero di Commenti',fontweight='bold')
plt.show()



# Filtra i commenti per ogni topic
cronaca = df[df['topic'].str.lower() == 'cronaca']
cronaca_nera = df[df['topic'].str.lower() == 'cronaca nera']
politica = df[df['topic'].str.lower() == 'politica']

# Definisci le categorie di commenti per ogni topic
categories = ['Positivi', 'Negativi', 'Hate Speech']

# Calcola il numero totale di commenti per ciascuna categoria e ciascun topic
totals_cronaca = [
    len(cronaca[cronaca['sentiment'] == 'positivo']),
    len(cronaca[cronaca['sentiment'] == 'negativo']),
    len(cronaca[cronaca['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])])
]

totals_cronaca_nera = [
    len(cronaca_nera[cronaca_nera['sentiment'] == 'positivo']),
    len(cronaca_nera[cronaca_nera['sentiment'] == 'negativo']),
    len(cronaca_nera[cronaca_nera['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])])
]

totals_politica = [
    len(politica[politica['sentiment'] == 'positivo']),
    len(politica[politica['sentiment'] == 'negativo']),
    len(politica[politica['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])])
]

# Crea il grafico a barre per ogni topic
plt.figure(figsize=(14, 6))

# Barre per il topic CRONACA
plt.bar([x - 0.2 for x in range(len(categories))], totals_cronaca, width=0.2, color='blue', label='CRONACA')
# Barre per il topic CRONACA NERA
plt.bar([x for x in range(len(categories))], totals_cronaca_nera, width=0.2, color='red', label='CRONACA NERA')
# Barre per il topic POLITICA
plt.bar([x + 0.2 for x in range(len(categories))], totals_politica, width=0.2, color='green', label='POLITICA')

plt.title('Numero Totale di Commenti per Categoria e Topic')
plt.xlabel('Categoria')
plt.ylabel('Numero di Commenti')
plt.xticks([0, 1, 2], categories)
plt.legend()
plt.show()
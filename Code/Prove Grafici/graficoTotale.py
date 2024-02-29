import pandas as pd
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

# Leggi il file CSV
df = pd.read_csv('/Users/roby/PycharmProjects/RetiGeografiche/commenti_dataset_a.csv')

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

import numpy as np

hate_speech_mapping = {'no': False, 'inappropriato': True, 'offensivo': True, 'violento': True}
df['hate_speech_flag'] = df['hate_speech'].map(hate_speech_mapping)

# Raggruppa i dati per sentiment e hate_speech e conta il numero di commenti in ciascun gruppo
counts = df.groupby(['sentiment', 'hate_speech_flag']).size().reset_index(name='count')

# Filtra i dati per ottenere il numero di commenti che sono di odio + positivi e odio + negativi
hate_positive_count = counts[(counts['hate_speech_flag'] == True) & (counts['sentiment'] == 'positivo')]['count'].sum()
hate_negative_count = counts[(counts['hate_speech_flag'] == True) & (counts['sentiment'] == 'negativo')]['count'].sum()

# Calcola il numero totale di commenti positivi e negativi
total_positive_count = len(df[df['sentiment'] == 'positivo'])
total_negative_count = len(df[df['sentiment'] == 'negativo'])

# Creazione del grafico a barre sovrapposte
bar_width = 0.35
index = np.arange(2)

# Creazione delle barre per i commenti positivi e negativi
# Creazione delle barre per i commenti positivi e negativi
plt.bar(index, [total_positive_count, total_negative_count], bar_width, color=['green', 'orange'], label=['Positivi', 'Negativi'])

# Creazione delle barre per i commenti di odio positivi e negativi
plt.bar(index, [hate_positive_count, hate_negative_count], bar_width, color=['red', 'red'], label='Odio')

plt.xlabel('Categorie', fontweight='bold')
plt.ylabel('Numero commenti',fontweight='bold')
plt.title('Commenti di Hate Speech e Sentiment',fontweight='bold')
plt.xticks(index, ['Positivi', 'Negativi'],fontweight='bold')
plt.legend()

# Aggiunta dei numeri sopra le barre
for i, value in enumerate([total_positive_count, total_negative_count, hate_positive_count, hate_negative_count]):
    plt.text(i % 2, value + 10, str(value), ha='center',fontweight='bold')

plt.show()
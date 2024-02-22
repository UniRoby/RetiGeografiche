
import pandas as pd
import matplotlib.pyplot as plt

# Leggi il file CSV
df = pd.read_csv('/Users/roby/PycharmProjects/RetiGeografiche/commenti_dataset_r.csv')

# Filtra i commenti positivi, negativi e di hate speech
commenti_positivi = df[df['sentiment'] == 'positivo']
commenti_negativi = df[df['sentiment'] == 'negativo']
commenti_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]

# Raggruppa per topic e calcola il numero di commenti per ogni categoria
grouped_positivi = commenti_positivi.groupby('topic').size()
grouped_negativi = commenti_negativi.groupby('topic').size()
grouped_hate_speech = commenti_hate_speech.groupby('topic').size()

# Prepara le categorie di commenti
categories = ['Positivi', 'Negativi', 'Hate Speech']
colors = ['green', 'orange', 'red']

# Crea il grafico
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(10, 18))

for i, (topic, data) in enumerate(grouped_positivi.items()):
    for j, cat in enumerate(categories):
        if cat == 'Positivi':
            axs[i].bar(cat, data, color=colors[j], label=cat)
        elif cat == 'Negativi':
            axs[i].bar(cat, grouped_negativi.get(topic, 0), color=colors[j], label=cat)
        elif cat == 'Hate Speech':
            axs[i].bar(cat, grouped_hate_speech.get(topic, 0), color=colors[j], label=cat)

    # Aggiungi etichette e titolo
    axs[i].set_xlabel('Categoria di Commenti')
    axs[i].set_ylabel('Numero di Commenti')
    axs[i].set_title(f'Topic: {topic}')

    # Nascondi la griglia
    axs[i].grid(False)

    # Aggiungi legenda
    axs[i].legend()

plt.tight_layout()
plt.show()


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leggi il file CSV
df = pd.read_csv('/Users/roby/PycharmProjects/RetiGeografiche/commenti_dataset_r.csv')


# Raggruppa per topic e calcola il numero di commenti positivi, negativi e di hate speech
grouped_data = df.groupby(['topic', 'sentiment']).size().unstack(fill_value=0)
grouped_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])].groupby('topic').size()

# Prepara i dati per il grafico
topics = grouped_data.index
positivi = grouped_data['positivo']
negativi = grouped_data['negativo']
hate_speech = grouped_hate_speech

# Prepara l'indice delle barre
bar_width = 0.25
index = np.arange(len(topics))

# Crea il grafico
plt.figure(figsize=(12, 6))

bars1 = plt.bar(index, positivi, bar_width, label='Positivi', color='green')
bars2 = plt.bar(index + bar_width, negativi, bar_width, label='Negativi', color='orange')
bars3 = plt.bar(index + bar_width * 2, hate_speech, bar_width, label='Hate Speech', color='red')

# Aggiungi etichette e titolo
plt.xlabel('Topic')
plt.ylabel('Numero di Commenti')
plt.title('Distribuzione dei Commenti per Categoria e Topic')
plt.xticks(index + bar_width, topics)
plt.grid(False)

# Aggiungi legenda
plt.legend()

# Aggiungi annotazioni
def autolabel(bars):
    for bar in bars:
        height = bar.get_height()
        plt.annotate('{}'.format(height),
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 3),
                     textcoords="offset points",
                     ha='center', va='bottom')

autolabel(bars1)
autolabel(bars2)
autolabel(bars3)

plt.tight_layout()
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leggi il nuovo dataset
df = pd.read_csv('commenti_dataset_r.csv')

# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]

# Numero di commenti negativi e positivi per ogni social
commenti_per_social = pd.crosstab(commenti_hate_speech['social'], commenti_hate_speech['sentiment'])

# Calcola la media dei commenti negativi per ogni social
media_negativi_per_social = commenti_per_social['negativo'] / commenti_per_social.sum(axis=1)

# Creazione del grafico a barre
fig, ax = plt.subplots(figsize=(10, 6))
media_negativi_per_social.plot(kind='bar', ax=ax, color='red', alpha=0.7)

# Aggiungi etichette al grafico
ax.set_title("Media Commenti Negativi per Ogni Social")
ax.set_xlabel("Social")
ax.set_ylabel("Percentuale di Commenti Negativi")
# Ruota le etichette degli assi x di 45 gradi
ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='right')
# Mostra il grafico
plt.show()




# Numero di commenti per ogni video (titolo)
commenti_per_video = df.groupby('titolo').size().reset_index(name='num_commenti')

# Numero di commenti positivi e negativi per ogni video (titolo)
commenti_positivi_negativi_per_video = df.groupby(['titolo', 'sentiment']).size().unstack(fill_value=0).reset_index()

# Numero di righe con negativo per ogni video/titolo e autore
num_commenti_negativi_per_titolo_e_autore = df[df['sentiment'] == 'negativo'].groupby(['autore', 'titolo']).size().reset_index(name='num_commenti_negativi')

# Calcola la media per ciascun autore
media_negativi_per_autore = num_commenti_negativi_per_titolo_e_autore.groupby('autore')['num_commenti_negativi'].mean()

# Seleziona solo i commenti positivi
commenti_positivi = df[df['sentiment'] == 'positivo']

# Conta il numero di commenti positivi per ciascun video/titolo e autore
num_commenti_positivi_per_titolo_e_autore = commenti_positivi.groupby(['autore', 'titolo']).size().reset_index(name='num_commenti_positivi')

# Calcola la media per ciascun autore
media_positivi_per_autore = num_commenti_positivi_per_titolo_e_autore.groupby('autore')['num_commenti_positivi'].mean()

# Stampa il risultato
for autore, media_negativi in media_negativi_per_autore.items():
    print(f'autore: {autore}, Media Commenti Negativi: {media_negativi:.2f}')

for autore, media_positivi in media_positivi_per_autore.items():
    print(f'autore: {autore}, Media Commenti Positivi: {media_positivi:.2f}')

# Numero di titoli diversi per lo stesso autore
num_titoli_per_autore = df.groupby('autore')['titolo'].nunique()
print("Numero di video diversi per autore:\n", num_titoli_per_autore)


# Commenti negativi e positivi per ogni topic
commenti_per_topic = df.groupby(['topic', 'sentiment']).size().unstack(fill_value=0)

# Stampa dei risultati
print("Numero di commenti per ogni video:")
print(commenti_per_video)

print("\nNumero di commenti positivi  e negativi per ogni video:")
print(commenti_positivi_negativi_per_video)



print("\nCommenti negativi e positivi per ogni topic:")
print(commenti_per_topic)

# Grafico a barre per il numero di commenti per ogni video (titolo)
commenti_per_video.plot(kind='bar', xlabel='Video (Titolo)', ylabel='Numero di commenti', title='Numero di commenti per ogni video')
plt.show()

# Grafico a barre empilato per commenti negativi e positivi per ogni video
commenti_per_video_neg_pos = pd.concat([commenti_positivi_negativi_per_video[0], commenti_positivi_negativi_per_video[0]], axis=1)
commenti_per_video_neg_pos.columns = ['Negativi', 'Positivi']
commenti_per_video_neg_pos.plot(kind='bar', stacked=True, xlabel='Video (Titolo)', ylabel='Numero di commenti', title='Commenti negativi e positivi per ogni video')
plt.show()

# Grafico a torta per la proporzione di commenti negativi e positivi per ogni topic
commenti_per_topic.plot(kind='pie', autopct='%1.1f%%', subplots=True, layout=(2, 2), legend=False, title='Proporzione di commenti negativi e positivi per ogni topic')
plt.show()

# Seleziona solo i commenti con hate_speech=1
commenti_negativi = df[df['hate_speech'] == 1]

# Conta il numero di commenti negativi per ciascun topic
num_commenti_negativi_per_topic = commenti_negativi['topic'].value_counts()

# Trova il topic con il massimo numero di commenti negativi
topic_max_commenti_negativi = num_commenti_negativi_per_topic.idxmax()
max_commenti_negativi = num_commenti_negativi_per_topic.max()

print(f"Topic con il maggior numero di commenti negativi: {topic_max_commenti_negativi}")
print(f"Numero di commenti negativi: {max_commenti_negativi}")

bar_width = 0.35
bar_positions_negativi = np.arange(len(media_negativi_per_autore))
bar_positions_positivi = bar_positions_negativi + bar_width


fig, ax = plt.subplots()
ax.bar(bar_positions_negativi, media_negativi_per_autore.values, width=bar_width, color='#1f77b4', label='Commenti Negativi')  # Blue
ax.bar(bar_positions_positivi, media_positivi_per_autore.values, width=bar_width, color='#ff7f0e', label='Commenti Positivi')  # Green


ax.set_title("Media Commenti Negativi e Positivi per Ogni Video")
ax.set_xlabel("autore")
ax.set_ylabel("Numero di Commenti")
ax.set_xticks(bar_positions_negativi + bar_width / 2)
ax.set_xticklabels(media_negativi_per_autore.index)
ax.legend()
plt.show()





# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo', 'violento'
commenti_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]

# Numero di commenti di hate_speech per ogni video (titolo)
commenti_hate_speech_per_video = commenti_hate_speech.groupby(['titolo', 'hate_speech']).size().unstack(fill_value=0).reset_index()

# Numero di righe con commenti di hate_speech per ogni video, titolo e autore
num_commenti_hate_speech_per_titolo_e_autore = commenti_hate_speech.groupby(['autore', 'titolo']).size().reset_index(name='num_commenti_hate_speech')


# Calcola la media dei commenti di hate_speech per ciascun autore
media_hate_speech_per_autore = num_commenti_hate_speech_per_titolo_e_autore.groupby('autore')['num_commenti_hate_speech'].mean()

# Visualizza il risultato
print(media_hate_speech_per_autore)
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leggi il file CSV
df = pd.read_csv('commenti_dataset.csv')

# Numero di commenti per ogni video (titolo)
commenti_per_video = df.groupby('titolo').size().reset_index(name='num_commenti')

# Numero di commenti positivi (hate_speech=0) e negativi (hate_speech=1) per ogni video (titolo)
commenti_positivi_negativi_per_video = df.groupby(['titolo', 'hate_speech']).size().unstack(fill_value=0).reset_index()

# Numero di righe con hate_speech=1 per ogni video/titolo e canale
num_commenti_negativi_per_titolo_e_canale = df[df['hate_speech'] == 1].groupby(['canale', 'titolo']).size().reset_index(name='num_commenti_negativi')

# Calcola la media per ciascun canale
media_negativi_per_canale = num_commenti_negativi_per_titolo_e_canale.groupby('canale')['num_commenti_negativi'].mean()


# Seleziona solo i commenti con hate_speech=0 (commenti positivi)
commenti_positivi = df[df['hate_speech'] == 0]

# Conta il numero di commenti positivi per ciascun video/titolo e canale
num_commenti_positivi_per_titolo_e_canale = commenti_positivi.groupby(['canale', 'titolo']).size().reset_index(name='num_commenti_positivi')

# Calcola la media per ciascun canale
media_positivi_per_canale = num_commenti_positivi_per_titolo_e_canale.groupby('canale')['num_commenti_positivi'].mean()

# Stampa il risultato
for canale, media_negativi in media_negativi_per_canale.items():
    print(f'Canale: {canale}, Media Commenti Negativi: {media_negativi:.2f}')

for canale, media_positivi in media_positivi_per_canale.items():
    print(f'Canale: {canale}, Media Commenti Positivi: {media_positivi:.2f}')

# Numero di titoli diversi per lo stesso canale
num_titoli_per_canale = df.groupby('canale')['titolo'].nunique()
print("Numero di video diversi per canale:\n", num_titoli_per_canale)


# Commenti negativi e positivi per ogni topic
commenti_per_topic = df.groupby(['topic', 'hate_speech']).size().unstack(fill_value=0)

# Stampa dei risultati
print("Numero di commenti per ogni video:")
print(commenti_per_video)

print("\nNumero di commenti positivi (hate_speech=0) e negativi (hate_speech=1) per ogni video (titolo):")
print(commenti_positivi_negativi_per_video)



print("\nCommenti negativi e positivi per ogni topic:")
print(commenti_per_topic)

# Grafico a barre per il numero di commenti per ogni video (titolo)
commenti_per_video.plot(kind='bar', xlabel='Video (Titolo)', ylabel='Numero di commenti', title='Numero di commenti per ogni video')
plt.show()

# Grafico a barre empilato per commenti negativi e positivi per ogni video
commenti_per_video_neg_pos = pd.concat([commenti_positivi_negativi_per_video[1], commenti_positivi_negativi_per_video[0]], axis=1)
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
bar_positions_negativi = np.arange(len(media_negativi_per_canale))
bar_positions_positivi = bar_positions_negativi + bar_width


fig, ax = plt.subplots()
ax.bar(bar_positions_negativi, media_negativi_per_canale.values, width=bar_width, color='#1f77b4', label='Commenti Negativi')  # Blue
ax.bar(bar_positions_positivi, media_positivi_per_canale.values, width=bar_width, color='#ff7f0e', label='Commenti Positivi')  # Green


ax.set_title("Media Commenti Negativi e Positivi per Ogni Video")
ax.set_xlabel("Canale")
ax.set_ylabel("Numero di Commenti")
ax.set_xticks(bar_positions_negativi + bar_width / 2)
ax.set_xticklabels(media_negativi_per_canale.index)
ax.legend()


plt.show()
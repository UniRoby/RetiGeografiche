import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leggi il file CSV
df = pd.read_csv('commenti_dataset_a.csv')

# Numero di righe negative per ogni notizia/titolo e giornale per social
num_commenti_negativi_per_titolo_e_giornale = df[df['sentiment'] == 'negativo'].groupby(['giornale', 'titolo','social']).size().reset_index(name='num_commenti_negativi')

# Calcola la media per ciascun giornale
media_negativi_per_giornale = num_commenti_negativi_per_titolo_e_giornale.groupby(['giornale','social'])['num_commenti_negativi'].mean()

# Seleziona solo i commenti positivi
commenti_positivi = df[df['sentiment'] == 'positivo']

# Conta il numero di commenti positivi per ciascuna notizia e giornale per social
num_commenti_positivi_per_titolo_e_giornale = commenti_positivi.groupby(['giornale', 'titolo','social']).size().reset_index(name='num_commenti_positivi')

# Calcola la media per ciascun giornale suddivisio per social
media_positivi_per_giornale = num_commenti_positivi_per_titolo_e_giornale.groupby(['giornale','social'])['num_commenti_positivi'].mean()


for giornale, media_negativi in media_negativi_per_giornale.items():
    print(f'Social, Giornale: {giornale}, Media Commenti Negativi: {media_negativi:.2f}')

for giornale, media_positivi in media_positivi_per_giornale.items():
    print(f'Social, Giornale: {giornale}, Media Commenti Positivi: {media_positivi:.2f}')

# Numero di titoli diversi per lo stesso giornale
num_titoli_per_giornale = df.groupby('giornale')['titolo'].nunique()
print("\nNumero di notizia diverse per giornale:\n", num_titoli_per_giornale)

# Numero di commenti per ogni notizia suddivise per giornale e topic (titolo) per social
commenti_per_notizia = df.groupby(['titolo', 'giornale','social']).size().reset_index(name='num_commenti')
# Stampa dei risultati
print("\nNumero di commenti per ogni notizia (suddivisi per giornale e social:")
print(commenti_per_notizia)

# Numero di commenti positivi e negativi per ogni notizia (titolo) per social
commenti_positivi_negativi_per_notizia = df.groupby(['titolo','giornale', 'social', 'sentiment']).size().unstack(fill_value=0).reset_index()
print("\n(Creare Excel) Numero di commenti positivi e negativi per ogni notizia:")
print(commenti_positivi_negativi_per_notizia)

# Commenti negativi e positivi per ogni topic
commenti_per_topic = df.groupby(['topic','social','sentiment']).size().unstack(fill_value=0).reset_index()
print("\nCommenti negativi e positivi per ogni topic per social:")
print(commenti_per_topic)

# Commenti di odio per ogni topic
commenti_hS_per_topic = df.groupby(['topic','social','hate_speech']).size().unstack(fill_value=0).reset_index()
print("\nCommenti hate speech per ogni topic per social suddivisi per categoria di odio:")
print(commenti_hS_per_topic)

# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]
# Conta il numero di commenti odio per ciascun topic
#num_commenti_hate_per_topic = commenti_hate_speech['topic'].value_counts()
num_commenti_hate_per_topic =commenti_hate_speech.groupby(['topic','social']).size().reset_index(name='num_hate_topic')
print("\nCommenti hate speech per ogni topic per social:")
print(num_commenti_hate_per_topic)

# Trova il topic con il massimo numero di commenti odio per ogni social

# Trova l'indice del massimo numero di commenti di odio per ogni social e topic
idx_max_hate = num_commenti_hate_per_topic.groupby('social')['num_hate_topic'].idxmax()
# Utilizza gli indici trovati per estrarre i corrispondenti topic con il massimo numero di commenti di odio per ogni social
topic_max_hate_per_social = num_commenti_hate_per_topic.loc[idx_max_hate]
# Stampa i risultati
print("\nTopic con il massimo numero di commenti di odio per ogni social:")
print(topic_max_hate_per_social)



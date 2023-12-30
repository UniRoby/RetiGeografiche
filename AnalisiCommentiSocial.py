import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Leggi il nuovo dataset
df = pd.read_csv('commenti_dataset.csv')

social=df['social'].tolist()
t=0
y=0
for s in social:
    if s=='Twitter':
        t+=1
    else:
        y+=1
print(f'----------- Numero righe Twitter: {t}\n----------- Numero righe Youtube: {y}')

# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]


# Numero di commenti negativi e positivi per ogni social
social_sentiment_counts = df.groupby(['social', 'sentiment']).size().unstack(fill_value=0)
print(f'----------- Numero di commenti negativi e positivi per ogni social: {social_sentiment_counts}\n')

# Calcola la media dei commenti negativi per ogni social
media_negativi_per_social = social_sentiment_counts['negativo'].mean()
print(f'----------- Media dei commenti negativi per ogni social: {media_negativi_per_social}\n')

# Calcola la media dei commenti positivi per ogni social
media_positivi_per_social = social_sentiment_counts['positivo'].mean()
print(f'----------- Media dei commenti positivi per ogni social: {media_positivi_per_social}\n')

# Calcola il numero di commenti di hate_speech per ogni social
hate_speech_counts_per_social = commenti_hate_speech.groupby('social').size()
print(f'----------- Numero di commenti di Hate Speech per ogni social: {hate_speech_counts_per_social}\n')

# Numero di post (titoli) distinti per ogni social
num_post_distinti_per_social = df.groupby('social')['titolo'].nunique()

# Calcola la media dei commenti di hate speech per ogni social
media_hate_speech_per_social = hate_speech_counts_per_social / num_post_distinti_per_social

# Stampa dei risultati
print("----------- Media Commenti di Hate Speech per Social: ")
print(media_hate_speech_per_social)



#------Sezione Social Youtube


# Numero di commenti positivi e negativi per ogni video (titolo) di Youtube

# Numero di righe con sentiment = negativo per ogni video/titolo e giornale di Youtube

# Calcola la media di commenti negativi per ciascun giornale di Youtube

# Seleziona solo i commenti con sentiment=positivo del social= Youtube

# Conta il numero di commenti positivi per ciascun video/titolo e giornale di Youtube

# Calcola la media per commenti positivi ciascun giornale di Youtube

# Numero di righe/commenti di hate_speech  per ogni video/titolo e giornale di Youtube

# Calcola la media per commenti di hate_speech ciascun giornale di Youtube

# Stampa dei risultati

#Stampa  numero di titoli diversi per lo stesso giornale di Youtube

# Commenti negativi, positivi, e di hate speech per ogni topic di Youtube

# Conta il numero di commenti di hate speech (commenti_hate_speech) per ciascun topic di Youtube

# Trova il topic con il massimo numero di commenti di hate speech

# Stampa dei risultati

# Numero di commenti per ogni video (titolo) e social == Youtube
commenti_per_video_youtube = df[df['social'] == 'YouTube'].groupby('titolo').size()
print(f'----------- Numero di commenti per ogni video di Youtube: {commenti_per_video_youtube }\n')

# Numero di commenti positivi e negativi per ogni video (titolo) di Youtube
sentiment_counts_youtube = df[df['social'] == 'YouTube'].groupby(['titolo', 'sentiment']).size().unstack(fill_value=0)
print(f'----------- Numero di commenti negativi e positivi per ogni video (titolo) di Youtube: {sentiment_counts_youtube }\n')


# Numero di righe con sentiment = negativo per ogni video/titolo e giornale di Youtube
num_commenti_negativi_per_titolo_e_giornale_youtube = df[(df['social'] == 'YouTube') & (df['sentiment'] == 'negativo')].groupby(['giornale', 'titolo']).size().reset_index(name='num_commenti_negativi')
print(f'----------- Numero di commenti negativi per ogni video/titolo e giornale  di Youtube: {num_commenti_negativi_per_titolo_e_giornale_youtube }\n')

# Calcola la media di commenti negativi per ciascun giornale di Youtube
media_negativi_per_giornale_youtube = num_commenti_negativi_per_titolo_e_giornale_youtube.groupby('giornale')['num_commenti_negativi'].mean()
print(f'----------- Media di commenti negativi per ciascun giornale di Youtube: {media_negativi_per_giornale_youtube }\n')

# Seleziona solo i commenti con sentiment=positivo del social= Youtube
commenti_positivi_youtube = df[(df['social'] == 'YouTube') & (df['sentiment'] == 'positivo')]
#print(f'----------- Numero di commenti commenti positivi di Youtube: {commenti_positivi_youtube }\n')

# Conta il numero di commenti positivi per ciascun video/titolo e giornale di Youtube
num_commenti_positivi_per_titolo_e_giornale_youtube = commenti_positivi_youtube.groupby(['giornale', 'titolo']).size().reset_index(name='num_commenti_positivi')
print(f'----------- Conta il numero di commenti positivi per ciascun video/titolo e giornale di Youtube: {num_commenti_positivi_per_titolo_e_giornale_youtube }\n')

# Calcola la media per commenti positivi ciascun giornale di Youtube
media_positivi_per_giornale_youtube = num_commenti_positivi_per_titolo_e_giornale_youtube.groupby('giornale')['num_commenti_positivi'].mean()
print(f'----------- Media per commenti positivi ciascun giornale di Youtube: {media_positivi_per_giornale_youtube }\n')

# Numero di righe/commenti di hate_speech  per ogni video/titolo e giornale di Youtube
num_commenti_hate_speech_per_titolo_e_giornale_youtube = commenti_hate_speech[commenti_hate_speech['social'] == 'YouTube'].groupby(['giornale', 'titolo']).size().reset_index(name='num_commenti_hate_speech')
print(f'----------- Numero di commenti di hate_speech per ogni video e giornale di Youtube: {num_commenti_hate_speech_per_titolo_e_giornale_youtube }\n')

# Calcola la media per commenti di hate_speech ciascun giornale di Youtube
media_hate_speech_per_giornale_youtube = num_commenti_hate_speech_per_titolo_e_giornale_youtube.groupby('giornale')['num_commenti_hate_speech'].mean()
print(f'----------- Media per commenti di hate_speech ciascun giornale di Youtube: {media_hate_speech_per_giornale_youtube }\n')







# Stampa numero di titoli diversi per lo stesso giornale di Youtube
num_titoli_per_canale = df[df['social'] == 'YouTube'].groupby('giornale')['titolo'].nunique()
print("Numero di video diversi per canale:\n", num_titoli_per_canale)

#-----Sezione Social Twitter

# Numero di commenti per ogni post (titolo) e social == Twitter

# Numero di commenti positivi e negativi per ogni post (titolo) di Twitter

# Numero di righe con sentiment = negativo per ogni post/titolo e giornale sul social= Twitter

# Calcola la media di commenti negativi per ciascun giornale di Twitter

# Seleziona solo i commenti con sentiment=positivo del social= Youtube

# Conta il numero di commenti positivi per ciascun video/titolo e giornale di Youtube

# Calcola la media di commenti positivi per ciascun giornale di Youtube

# Numero di righe/commenti di hate_speech per ogni post/titolo e giornale di Twitter

# Calcola la media per commenti di hate_speech ciascun giornale di Twitter

# Stampa dei risultati

#Stampa  numero di titoli diversi per lo stesso giornale di Twitter

# Commenti negativi, positivi, e di hate speech per ogni topic di Twitter

# Conta il numero di commenti di hate speech (commenti_hate_speech) per ciascun topic di Twitter

# Trova il topic con il massimo numero di commenti di hate speech

# Stampa dei risultati
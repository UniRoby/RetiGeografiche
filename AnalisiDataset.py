import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def create_excel(csv_file, excel_filename, description):
    # Verifica se il file esiste già
    if not os.path.exists(
            "File_Excel/" + excel_filename + ".xlsx"):  # Utilizza il percorso relativo e aggiungi l'estensione ".xlsx"
        # Aggiungi una riga di descrizione al DataFrame
        csv_file = pd.concat([pd.DataFrame([description]), csv_file], ignore_index=True)

        # Salva i dati nel file Excel solo se il file non esiste già
        csv_file.to_excel("File_Excel/" + excel_filename + ".xlsx",
                          index=False)  # Assicurati di salvare con l'estensione corretta
        print(f"I dati sono stati salvati con successo in 'File_Excel/{excel_filename}.xlsx'.")
    else:
        print(f"Il file '{excel_filename}' esiste già. Non è stato creato un nuovo file.")
def topicPercentage(df):
    # Calcola il numero totale di commenti per ogni argomento
    num_commenti_per_topic = df.groupby(['topic', 'social']).size().reset_index(name='num_commenti_per_topic')

    # Calcola il numero di commenti di odio per ogni argomento
    num_commenti_hate_per_topic = commenti_hate_speech.groupby(['topic', 'social']).size().reset_index(
        name='num_hate_topic')

    # Unisci i due DataFrame in base alla colonna 'topic' e 'social'
    merged_df = pd.merge(num_commenti_per_topic, num_commenti_hate_per_topic, on=['topic', 'social'], how='left')

    # Calcola la percentuale di commenti di odio per ogni argomento rispetto al numero totale di commenti per quell'argomento
    merged_df['percentuale_hate_per_topic'] = (
                (merged_df['num_hate_topic'] / merged_df['num_commenti_per_topic']) * 100).round(2)

    # Aggiungi il simbolo '%' al valore della percentuale
    merged_df['percentuale_hate_per_topic'] = merged_df['percentuale_hate_per_topic'].astype(str) + '%'

    # Stampa i risultati
    print("\nPercentuale di commenti di odio per ogni argomento per social:")
    print(merged_df)


# Leggi il file CSV
df = pd.read_csv('commenti_dataset.csv')

# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]


# Numero di titoli diversi per lo stesso giornale
num_titoli_per_giornale = df.groupby('giornale')['titolo'].nunique()
print("\nNumero di notizia diverse per giornale:\n", num_titoli_per_giornale)

# Numero di commenti per ogni notizia suddivise per giornale e topic (titolo) per social
commenti_per_notizia = df.groupby(['titolo', 'giornale','social']).size().reset_index(name='num_commenti')
# Stampa dei risultati
print("\nNumero di commenti per ogni notizia (suddivisi per giornale e social:")
print(commenti_per_notizia)
#Excel
create_excel(commenti_per_notizia,"commenti_per_notizia","Numero di commenti per ogni notizia (suddivisi per giornale e social")


# Numero di commenti positivi e negativi per ogni notizia (titolo) per social
commenti_positivi_negativi_per_notizia = df.groupby(['titolo','giornale', 'social', 'sentiment']).size().unstack(fill_value=0).reset_index()
print("\nNumero di commenti positivi e negativi per ogni notizia:")
print(commenti_positivi_negativi_per_notizia)
#Excel
create_excel(commenti_positivi_negativi_per_notizia,"commenti_positivi_negativi_per_notizia","Numero di commenti positivi e negativi per ogni notizia")



# Numero di commenti di odio per ogni notizia suddivise per giornale e topic (titolo) per social
commenti_odio_per_notizia = commenti_hate_speech.groupby(['titolo', 'giornale','social']).size().reset_index(name='hate_speech')
# Stampa dei risultati
print("\nNumero di commenti odio per ogni notizia (suddivisi per giornale e social):")
print(commenti_odio_per_notizia)
#Excel
create_excel(commenti_odio_per_notizia,"commenti_odio_per_notizia","Numero di commenti odio per ogni notizia (suddivisi per giornale e social)")



# Commenti negativi e positivi per ogni topic
commenti_per_topic = df.groupby(['topic','social','sentiment']).size().unstack(fill_value=0).reset_index()
print("\nCommenti negativi e positivi per ogni topic per social:")
print(commenti_per_topic)
#Excel
create_excel(commenti_per_topic,"commenti_per_topic","Commenti negativi e positivi per ogni topic per social")

# Commenti di odio per ogni topic
commenti_hS_per_topic = df.groupby(['topic','social','hate_speech']).size().unstack(fill_value=0).reset_index()
print("\nCommenti hate speech per ogni topic per social suddivisi per categoria di odio:")
print(commenti_hS_per_topic)
#Excel
create_excel(commenti_hS_per_topic,"commenti_hS_per_topic","Commenti hate speech per ogni topic per social suddivisi per categoria di odio")


# Conta il numero di commenti odio per ciascun topic
#num_commenti_hate_per_topic = commenti_hate_speech['topic'].value_counts()
num_commenti_hate_per_topic =commenti_hate_speech.groupby(['topic','social']).size().reset_index(name='num_hate_topic')
print("\nCommenti hate speech per ogni topic per social:  Mettere %")
print(num_commenti_hate_per_topic)
#Excel
create_excel(num_commenti_hate_per_topic,"num_commenti_hate_per_topic","Commenti hate speech per ogni topic per social")

topicPercentage(df)

# Trova il topic con il massimo numero di commenti odio per ogni social
# Trova l'indice del massimo numero di commenti di odio per ogni social e topic
idx_max_hate = num_commenti_hate_per_topic.groupby('social')['num_hate_topic'].idxmax()
# Utilizza gli indici trovati per estrarre i corrispondenti topic con il massimo numero di commenti di odio per ogni social
topic_max_hate_per_social = num_commenti_hate_per_topic.loc[idx_max_hate]
# Stampa i risultati
print("\nTopic con il massimo numero di commenti di odio per ogni social:")
print(topic_max_hate_per_social)


#-------------------------CRONACA-----------------------

cronaca = df[df['topic'].str.lower() == 'cronaca']
# Numero di commenti per ogni notizia (titolo) per social TOPIC=CRONACA
commenti_positivi_negativi_per_notizia_cronaca= cronaca.groupby(['topic','titolo','giornale', 'social','sentiment']).size().unstack(fill_value=0).reset_index()
print("\nNumero di commenti positivi e negativi per ogni notizia (CRONACA):")
print(commenti_positivi_negativi_per_notizia_cronaca)
#Excel
create_excel(commenti_positivi_negativi_per_notizia_cronaca,"commenti_positivi_negativi_per_notizia_cronaca","Numero di commenti positivi e negativi per ogni notizia (CRONACA)")


# Numero di commenti per ogni notizia suddivise per giornale e topic (titolo) per social TOPIC=CRONACA
commenti_per_notizia_cronaca = cronaca.groupby(['titolo', 'giornale','social']).size().reset_index(name='num_commenti')
# Stampa dei risultati
print("\nNumero di commenti per ogni notizia (suddivisi per giornale e social) (cronaca):")
print(commenti_per_notizia_cronaca)
#Excel
create_excel(commenti_per_notizia_cronaca,"commenti_per_notizia_cronaca","Numero di commenti per ogni notizia (suddivisi per giornale e social) (CRONACA)")


# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech_cronaca = cronaca[cronaca['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]

# Numero di commenti di odio per ogni notizia suddivise per giornale e topic (titolo) per social
commenti_odio_per_notizia_cronaca = commenti_hate_speech_cronaca.groupby(['titolo', 'giornale','social']).size().reset_index(name='hate_speech')
# Stampa dei risultati
print("\nNumero di commenti odio per ogni notizia (suddivisi per giornale e social)  (cronaca) :")
print(commenti_odio_per_notizia_cronaca)
#Excel
create_excel(commenti_odio_per_notizia_cronaca,"commenti_odio_per_notizia_cronaca","Numero di commenti odio per ogni notizia (suddivisi per giornale e social) (CRONACA)")


#-------------------------CRONACA NERA-----------------------

cronaca_nera = df[df['topic'].str.lower() == 'cronaca nera']
# Numero di commenti per ogni notizia (titolo) per social TOPIC=CRONACA_NERA
commenti_positivi_negativi_per_notizia_cronaca_nera= cronaca_nera.groupby(['topic','titolo','giornale', 'social','sentiment']).size().unstack(fill_value=0).reset_index()
print("\nNumero di commenti positivi e negativi per ogni notizia (CRONACA NERA):")
print(commenti_positivi_negativi_per_notizia_cronaca_nera)
#Excel
create_excel(commenti_positivi_negativi_per_notizia_cronaca_nera,"commenti_positivi_negativi_per_notizia_cronaca_nera","Numero di commenti positivi e negativi per ogni notizia (CRONACA NERA)")

# Numero di commenti per ogni notizia suddivise per giornale e topic (titolo) per social TOPIC=cronaca_nera
commenti_per_notizia_cronaca_nera = cronaca_nera.groupby(['titolo', 'giornale','social']).size().reset_index(name='num_commenti')
# Stampa dei risultati
print("\nNumero di commenti per ogni notizia (suddivisi per giornale e social) (cronaca_nera):")
print(commenti_per_notizia_cronaca_nera)
#Excel
create_excel(commenti_per_notizia_cronaca_nera,"commenti_per_notizia_cronaca_nera","Numero di commenti per ogni notizia (suddivisi per giornale e social) (CRONACA NERA)")

# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech_cronaca_nera = cronaca_nera[cronaca_nera['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]
# Numero di commenti di odio per ogni notizia suddivise per giornale e topic (titolo) per social
commenti_odio_per_notizia_cronaca_nera = commenti_hate_speech_cronaca_nera.groupby(['titolo', 'giornale','social']).size().reset_index(name='hate_speech')
# Stampa dei risultati
print("\nNumero di commenti odio per ogni notizia (suddivisi per giornale e social  (cronaca_nera) :")
print(commenti_odio_per_notizia_cronaca_nera)
#Excel
create_excel(commenti_odio_per_notizia_cronaca_nera,"commenti_odio_per_notizia_cronaca_nera","Numero di commenti odio per ogni notizia (suddivisi per giornale e social (CRONACA NERA)")


#-------------------------POLITICA-----------------------

politica = df[df['topic'].str.lower() == 'politica']
# Numero di commenti per ogni notizia (titolo) per social TOPIC=politica
commenti_positivi_negativi_per_notizia_politica= politica.groupby(['topic','titolo','giornale', 'social','sentiment']).size().unstack(fill_value=0).reset_index()
print("\nNumero di commenti positivi e negativi per ogni notizia (POLITICA):")
print(commenti_positivi_negativi_per_notizia_politica)
#Excel
create_excel(commenti_positivi_negativi_per_notizia_politica,"commenti_positivi_negativi_per_notizia_politica","Numero di commenti positivi e negativi per ogni notizia (POLITICA)")

# Numero di commenti per ogni notizia suddivise per giornale e topic (titolo) per social TOPIC=politica
commenti_per_notizia_politica = politica.groupby(['titolo', 'giornale','social']).size().reset_index(name='num_commenti')
# Stampa dei risultati
print("\nNumero di commenti per ogni notizia (suddivisi per giornale e social) (politica):")
print(commenti_per_notizia_politica)
#Excel
create_excel(commenti_per_notizia_politica,"commenti_per_notizia_politica","Numero di commenti per ogni notizia (suddivisi per giornale e social) (POLITICA)")

# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech_politica = politica[politica['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]
# Numero di commenti di odio per ogni notizia suddivise per giornale e topic (titolo) per social
commenti_odio_per_notizia_politica= commenti_hate_speech_politica.groupby(['titolo', 'giornale','social']).size().reset_index(name='hate_speech')
# Stampa dei risultati
print("\nNumero di commenti odio per ogni notizia (suddivisi per giornale e social)  (politica) :")
print(commenti_odio_per_notizia_politica)
#Excel
create_excel(commenti_odio_per_notizia_politica,"commenti_odio_per_notizia_politica","Numero di commenti odio per ogni notizia (suddivisi per giornale e social) (POLITICA)")


#--------------------------------------------------------------------------MEDIE------------------------------------------------------------------------------------------


# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]

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






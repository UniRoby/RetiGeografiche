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

def create_generic_histogram(df,xlabel_title,ylabel_title,topic):
    # Iterazione sui titoli delle notizie uniche nel DataFrame
    for titolo in df['titolo'].unique():
        # Selezionare i dati relativi a un titolo specifico
        df_subset = df[df['titolo'] == titolo]

        # Creazione del grafico a barre con gruppi affiancati
        fig, ax = plt.subplots()

        # Raggruppamento per social e giornale e calcolo del numero di commenti
        commenti_per_social_giornale = df_subset.groupby(['social', 'giornale'])['num_commenti'].sum().unstack(
            fill_value=0)

        # Calcolo delle posizioni dei gruppi di barre
        ind = range(len(commenti_per_social_giornale.index))

        # Creazione delle barre per ogni combinazione di social e giornale
        width = 0.2
        for i, col in enumerate(commenti_per_social_giornale.columns):
            ax.bar([x + width * i for x in ind], commenti_per_social_giornale[col], width=width, label=col)

        # Impostazione del titolo in grassetto
        ax.set_title(f'"{titolo}" - Topic: {topic}', fontweight='bold')

        ax.set_xlabel(xlabel_title, fontweight='bold')  # Impostazione dell'etichetta sull'asse x in grassetto
        ax.set_ylabel(ylabel_title, fontweight='bold')  # Impostazione dell'etichetta sull'asse y in grassetto

        # Impostazione delle etichette della legenda
        ax.legend(title='Giornale', loc='upper center', bbox_to_anchor=(0.5, -0.15),
                  ncol=len(commenti_per_social_giornale.columns))

        # Impostazione delle etichette sull'asse x
        ax.set_xticks([x + 0.2 for x in ind])
        ax.set_xticklabels(commenti_per_social_giornale.index)

        plt.xticks(rotation=0)

        # Regolazione dei margini
        plt.tight_layout()

        # Visualizzazione del grafico
        plt.show()

#xlabel= giornale
#ylabel=numero commenti
def create_negative_positive_histogram(df,xlabel_title,ylabel_title,topic):
    # Iterazione sui titoli delle notizie uniche nel DataFrame
    for titolo in df['titolo'].unique():
        # Selezionare i dati relativi a un titolo specifico
        print(titolo)
        df_subset = df[df['titolo'] == titolo]
        print(df_subset)
        grouped_df = df_subset.groupby(['giornale', 'social']).sum()

        # Estrazione dei valori per le etichette sull'asse x e i valori dei commenti
        giornali = df_subset['giornale'].unique()
        socials = df_subset['social'].unique()
        n_giornali = len(giornali)
        n_socials = len(socials)
        width = 0.2
        space = 0.01  # Spazio tra le barre dello stesso gruppo
        total_width = width * n_socials + space * (n_socials - 1)  # Larghezza complessiva dei gruppi di barre
        ind = np.arange(n_giornali)

        # Definizione dei colori per i social
        colors = {
            'Facebook': ('#5e6bda', '#338ee0'),  # Colore scuro e chiaro per Facebook
            'Instagram': ('#e5639c', '#efaeca'),  # Colore scuro e chiaro per Instagram
            'YouTube': ('#ac2b2b', '#df1818')  # Colore scuro e chiaro per YouTube
        }

        # Creazione del grafico a barre
        fig, ax = plt.subplots()

        # Iterazione su ogni social per creare le barre
        for i, social in enumerate(socials):
            positivi = []
            negativi = []
            for giornale in giornali:
                positivi.append(grouped_df.loc[giornale, social]['positivo'])
                negativi.append(grouped_df.loc[giornale, social]['negativo'])

            ax.bar(ind + i * (total_width + space) / n_socials + i * space / (n_socials - 1), negativi, width,
                   label=f'{social} - Negativi', color=colors[social][0])
            ax.bar(ind + i * (total_width + space) / n_socials + i * space / (n_socials - 1), positivi, width,
                   label=f'{social} - Positivi', bottom=negativi, color=colors[social][1])

        # Impostazione delle etichette sugli assi
        ax.set_xlabel(xlabel_title, fontweight='bold')
        ax.set_ylabel(ylabel_title, fontweight='bold')
        ax.set_title(f'"{titolo}" - Topic: {topic}', fontweight='bold')
        ax.set_xticks(ind + width / 2)
        ax.set_xticklabels(giornali)

        ax.legend(title='Commenti', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
        # Visualizzazione del grafico
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.show()

# Leggi il file CSV
df = pd.read_csv('commenti_dataset_r.csv')

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
#grafico
#create_generic_histogram(commenti_per_notizia,"Istogramma - Numero di commenti per ogni notizia (suddivisi per giornale e social)","Notizia","Numero di commenti")


# Numero di commenti positivi e negativi per ogni notizia (titolo) per social
commenti_positivi_negativi_per_notizia = df.groupby(['titolo','giornale', 'social', 'sentiment']).size().unstack(fill_value=0).reset_index()
print("\nNumero di commenti positivi e negativi per ogni notizia:")
print(commenti_positivi_negativi_per_notizia)
#Excel
create_excel(commenti_positivi_negativi_per_notizia,"commenti_positivi_negativi_per_notizia","Numero di commenti positivi e negativi per ogni notizia")
#Grafico
#create_generic_histogram(commenti_positivi_negativi_per_notizia,"Istogramma - Numero di commenti positivi e negativi per ogni notizia","Notizia","Numero di commenti")



# Numero di commenti di odio per ogni notizia suddivise per giornale e topic (titolo) per social
commenti_odio_per_notizia = commenti_hate_speech.groupby(['titolo', 'giornale','social']).size().reset_index(name='hate_speech')
# Stampa dei risultati
print("\nNumero di commenti odio per ogni notizia (suddivisi per giornale e social):")
print(commenti_odio_per_notizia)
#Excel
create_excel(commenti_odio_per_notizia,"commenti_odio_per_notizia","Numero di commenti odio per ogni notizia (suddivisi per giornale e social)")
#Grafico
#create_generic_histogram(commenti_odio_per_notizia,"Istogramma - Numero di commenti odio per ogni notizia (suddivisi per giornale e social)","Notizia","Numero di commenti odio")



# Commenti negativi e positivi per ogni topic
commenti_per_topic = df.groupby(['topic','social','sentiment']).size().unstack(fill_value=0).reset_index()
print("\nCommenti negativi e positivi per ogni topic per social:")
print(commenti_per_topic)
#Excel
create_excel(commenti_per_topic,"commenti_per_topic","Commenti negativi e positivi per ogni topic per social")
#Grafico
#create_generic_histogram(commenti_per_topic,"Istogramma - Commenti negativi e positivi per ogni topic per social","Topic","Numero di commenti")


# Commenti di odio per ogni topic
commenti_hS_per_topic = df.groupby(['topic','social','hate_speech']).size().unstack(fill_value=0).reset_index()
print("\nCommenti hate speech per ogni topic per social suddivisi per categoria di odio:")
print(commenti_hS_per_topic)
#Excel
create_excel(commenti_hS_per_topic,"commenti_hS_per_topic","Commenti hate speech per ogni topic per social suddivisi per categoria di odio")
#Grafico
#create_generic_histogram(commenti_hS_per_topic,"Istogramma - Commenti hate speech per ogni topic per social suddivisi per categoria di odio","Topic","Numero di commenti hate speech")


# Conta il numero di commenti odio per ciascun topic
#num_commenti_hate_per_topic = commenti_hate_speech['topic'].value_counts()
num_commenti_hate_per_topic =commenti_hate_speech.groupby(['topic','social']).size().reset_index(name='num_hate_topic')
print("\nCommenti hate speech per ogni topic per social:  Mettere %")
print(num_commenti_hate_per_topic)
#Excel
create_excel(num_commenti_hate_per_topic,"num_commenti_hate_per_topic","Commenti hate speech per ogni topic per social")
#Grafico
#create_generic_histogram(num_commenti_hate_per_topic,"Istogramma - Commenti hate speech per ogni topic per social","Topic","Percentuale di commenti hate speech")


topicPercentage(df)
#Grafico


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
#Grafico
create_negative_positive_histogram(commenti_positivi_negativi_per_notizia_cronaca,"Giornale","Numero Commenti","CRONACA")


# Numero di commenti per ogni notizia suddivise per giornale e topic (titolo) per social TOPIC=CRONACA
commenti_per_notizia_cronaca = cronaca.groupby(['titolo', 'giornale','social']).size().reset_index(name='num_commenti')
# Stampa dei risultati
print("\nNumero di commenti per ogni notizia (suddivisi per giornale e social) (cronaca):")
print(commenti_per_notizia_cronaca)
#Excel
create_excel(commenti_per_notizia_cronaca,"commenti_per_notizia_cronaca","Numero di commenti per ogni notizia (suddivisi per giornale e social) (CRONACA)")
#Grafico
create_generic_histogram(commenti_per_notizia_cronaca,"Social","Numero Commenti","CRONACA")


# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech_cronaca = cronaca[cronaca['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]

# Numero di commenti di odio per ogni notizia suddivise per giornale e topic (titolo) per social
commenti_odio_per_notizia_cronaca = commenti_hate_speech_cronaca.groupby(['titolo', 'giornale','social']).size().reset_index(name='hate_speech')
# Stampa dei risultati
print("\nNumero di commenti odio per ogni notizia (suddivisi per giornale e social)  (cronaca) :")
print(commenti_odio_per_notizia_cronaca)
#Excel
create_excel(commenti_odio_per_notizia_cronaca,"commenti_odio_per_notizia_cronaca","Numero di commenti odio per ogni notizia (suddivisi per giornale e social) (CRONACA)")
#Grafico
create_generic_histogram(commenti_odio_per_notizia_cronaca,"Istogramma - Numero di commenti odio per ogni notizia (suddivisi per giornale e social) (cronaca)","Notizia","Numero di commenti odio")


#-------------------------CRONACA NERA-----------------------

cronaca_nera = df[df['topic'].str.lower() == 'cronaca nera']
# Numero di commenti per ogni notizia (titolo) per social TOPIC=CRONACA_NERA
commenti_positivi_negativi_per_notizia_cronaca_nera= cronaca_nera.groupby(['topic','titolo','giornale', 'social','sentiment']).size().unstack(fill_value=0).reset_index()
print("\nNumero di commenti positivi e negativi per ogni notizia (CRONACA NERA):")
print(commenti_positivi_negativi_per_notizia_cronaca_nera)
#Excel
create_excel(commenti_positivi_negativi_per_notizia_cronaca_nera,"commenti_positivi_negativi_per_notizia_cronaca_nera","Numero di commenti positivi e negativi per ogni notizia (CRONACA NERA)")
#Grafico
create_negative_positive_histogram(commenti_positivi_negativi_per_notizia_cronaca_nera,"Giornale","Numero Commenti","CRONACA NERA")

# Numero di commenti per ogni notizia suddivise per giornale e topic (titolo) per social TOPIC=cronaca_nera
commenti_per_notizia_cronaca_nera = cronaca_nera.groupby(['titolo', 'giornale','social']).size().reset_index(name='num_commenti')
# Stampa dei risultati
print("\nNumero di commenti per ogni notizia (suddivisi per giornale e social) (cronaca_nera):")
print(commenti_per_notizia_cronaca_nera)
#Excel
create_excel(commenti_per_notizia_cronaca_nera,"commenti_per_notizia_cronaca_nera","Numero di commenti per ogni notizia (suddivisi per giornale e social) (CRONACA NERA)")
#Grafico
create_generic_histogram(commenti_per_notizia_cronaca_nera,"Social","Numero Commenti","CRONACA NERA")


# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech_cronaca_nera = cronaca_nera[cronaca_nera['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]
# Numero di commenti di odio per ogni notizia suddivise per giornale e topic (titolo) per social
commenti_odio_per_notizia_cronaca_nera = commenti_hate_speech_cronaca_nera.groupby(['titolo', 'giornale','social']).size().reset_index(name='hate_speech')
# Stampa dei risultati
print("\nNumero di commenti odio per ogni notizia (suddivisi per giornale e social  (cronaca_nera) :")
print(commenti_odio_per_notizia_cronaca_nera)
#Excel
create_excel(commenti_odio_per_notizia_cronaca_nera,"commenti_odio_per_notizia_cronaca_nera","Numero di commenti odio per ogni notizia (suddivisi per giornale e social (CRONACA NERA)")
#Grafico
create_generic_histogram(commenti_odio_per_notizia_cronaca_nera,"Istogramma - Numero di commenti odio per ogni notizia (suddivisi per giornale e social) (cronaca_nera)","Notizia","Numero di commenti odio")


#-------------------------POLITICA-----------------------

politica = df[df['topic'].str.lower() == 'politica']
# Numero di commenti per ogni notizia (titolo) per social TOPIC=politica
commenti_positivi_negativi_per_notizia_politica= politica.groupby(['topic','titolo','giornale', 'social','sentiment']).size().unstack(fill_value=0).reset_index()
print("\nNumero di commenti positivi e negativi per ogni notizia (POLITICA):")
print(commenti_positivi_negativi_per_notizia_politica)
#Excel
create_excel(commenti_positivi_negativi_per_notizia_politica,"commenti_positivi_negativi_per_notizia_politica","Numero di commenti positivi e negativi per ogni notizia (POLITICA)")
#Grafico
create_negative_positive_histogram(commenti_positivi_negativi_per_notizia_politica,"Giornale","Numero Commenti","POLITICA")

# Numero di commenti per ogni notizia suddivise per giornale e topic (titolo) per social TOPIC=politica
commenti_per_notizia_politica = politica.groupby(['titolo', 'giornale','social']).size().reset_index(name='num_commenti')
# Stampa dei risultati
print("\nNumero di commenti per ogni notizia (suddivisi per giornale e social) (politica):")
print(commenti_per_notizia_politica)
#Excel
create_excel(commenti_per_notizia_politica,"commenti_per_notizia_politica","Numero di commenti per ogni notizia (suddivisi per giornale e social) (POLITICA)")
#Grafico
create_generic_histogram(commenti_per_notizia_politica,"Social","Numero Commenti","POLITICA")

# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech_politica = politica[politica['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]
# Numero di commenti di odio per ogni notizia suddivise per giornale e topic (titolo) per social
commenti_odio_per_notizia_politica= commenti_hate_speech_politica.groupby(['titolo', 'giornale','social']).size().reset_index(name='hate_speech')
# Stampa dei risultati
print("\nNumero di commenti odio per ogni notizia (suddivisi per giornale e social)  (politica) :")
print(commenti_odio_per_notizia_politica)
#Excel
create_excel(commenti_odio_per_notizia_politica,"commenti_odio_per_notizia_politica","Numero di commenti odio per ogni notizia (suddivisi per giornale e social) (POLITICA)")
#Grafico
#create_generic_histogram(commenti_odio_per_notizia_politica,"Istogramma - Numero di commenti odio per ogni notizia (suddivisi per giornale e social) (politica)","Notizia","Numero di commenti odio")


#--------------------------------------------------------------------------MEDIE------------------------------------------------------------------------------------------


# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]

# Numero di righe negative per ogni notizia/titolo e giornale per social
num_commenti_negativi_per_titolo_e_giornale = df[df['sentiment'] == 'negativo'].groupby(['giornale', 'titolo','social']).size().reset_index(name='num_commenti_negativi')

# Calcola la media per ciascun giornale
media_negativi_per_giornale = num_commenti_negativi_per_titolo_e_giornale.groupby(['giornale','social'])['num_commenti_negativi'].mean()
#Grafico
#create_generic_histogram(media_negativi_per_giornale,"Istogramma - Media Commenti Negativi per Social e Giornale","Giornale","Media Commenti Negativi")

# Seleziona solo i commenti positivi
commenti_positivi = df[df['sentiment'] == 'positivo']

# Conta il numero di commenti positivi per ciascuna notizia e giornale per social
num_commenti_positivi_per_titolo_e_giornale = commenti_positivi.groupby(['giornale', 'titolo','social']).size().reset_index(name='num_commenti_positivi')

# Calcola la media per ciascun giornale suddivisio per social
media_positivi_per_giornale = num_commenti_positivi_per_titolo_e_giornale.groupby(['giornale','social'])['num_commenti_positivi'].mean()
#Grafico
#create_generic_histogram(media_positivi_per_giornale,"Istogramma - Media Commenti Positivi per Social e Giornale","Giornale","Media Commenti Positivi")


for giornale, media_negativi in media_negativi_per_giornale.items():
    print(f'Social, Giornale: {giornale}, Media Commenti Negativi: {media_negativi:.2f}')

for giornale, media_positivi in media_positivi_per_giornale.items():
    print(f'Social, Giornale: {giornale}, Media Commenti Positivi: {media_positivi:.2f}')





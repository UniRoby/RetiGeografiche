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
    


def create_count_histogram(df,xlabel_title,ylabel_title,topic):
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


def create_topic_comments_category_histogram(df):
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
    plt.xlabel('Topic', fontweight='bold')
    plt.ylabel('Numero di Commenti',fontweight='bold')
    plt.title('Distribuzione dei Commenti per Categoria e Topic',fontweight='bold')
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
    plt.savefig('IMAGES/topic_comments_category.png')
    plt.show()

def create_total_comments_category_histogram(df,commenti_hate_speech):
    # Filtra i commenti positivi, negativi e di hate speech
    commenti_positivi = df[df['sentiment'] == 'positivo']
    commenti_negativi = df[df['sentiment'] == 'negativo']

    # Calcola il numero totale di commenti per ciascuna categoria
    total_positivi = len(commenti_positivi)
    total_negativi = len(commenti_negativi)
    total_hate_speech = len(commenti_hate_speech)

    categories = ['Positivi', 'Negativi', 'Hate Speech']
    totals = [total_positivi, total_negativi, total_hate_speech]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, totals, color=['green', 'orange', 'red'])
    plt.title('Numero Totale di commenti per categoria', fontweight='bold')
    plt.xlabel('Categoria', fontweight='bold')
    plt.ylabel('Numero di Commenti', fontweight='bold')

    # Aggiungi il numero di commenti sopra ogni barra
    for bar, total in zip(bars, totals):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), total, ha='center', va='bottom', color='black',
                 fontsize=10)

    plt.savefig('IMAGES/total_comments_category.png')
    plt.show()


#xlabel= giornale
#ylabel=numero commenti
def create_negative_positive_histogram(df,topic):
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
            'Facebook': ('#3b5998', '#1877f2'),  # Colore scuro e chiaro per Facebook
            'Instagram': ('#c32aa3', '#efaeca'),  # Colore scuro e chiaro per Instagram
            'YouTube': ('#ac2b2b', '#ff0000')  # Colore scuro e chiaro per YouTube
        }

        # Creazione del grafico a barre
        fig, ax = plt.subplots()

        for i, social in enumerate(socials):
            positivi = []
            negativi = []
            for giornale in giornali:
                positivi.append(grouped_df.loc[giornale, social]['positivo'])
                negativi.append(grouped_df.loc[giornale, social]['negativo'])

            ax.bar(ind + i * (total_width + space) / n_socials + i * space / (n_socials - 1), negativi, width,
                   label=f'{social} - Negativi', color=colors[social][0])
            ax.bar(ind + i * (total_width + space) / n_socials + i * space / (n_socials - 1), positivi, width,
                   label=f'{social} - Positivi', bottom=np.zeros(len(positivi)),
                   color=colors[social][1])  # Imposta il bottom a un array di zeri

            # Aggiungi il numero di commenti negativi sopra ogni barra dei commenti negativi
            for j, neg in enumerate(negativi):
                ax.annotate(f"{neg}",
                            xy=(ind[j] + i * (total_width + space) / n_socials + i * space / (n_socials - 1), neg),
                            ha='center', va='bottom')

            # Aggiungi il numero di commenti positivi sopra o vicino ogni barra dei commenti positivi
            for j, pos in enumerate(positivi):
                ax.annotate(f"{pos}",
                            xy=(ind[j] + i * (total_width + space) / n_socials + i * space / (n_socials - 1), pos),
                            ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', color='black',
                            fontsize=8)

        # Impostazione delle etichette sugli assi
        ax.set_xlabel("Giornale", fontweight='bold')
        ax.set_ylabel("Numero Commenti", fontweight='bold')
        ax.set_title(f'"{titolo}" - Topic: {topic}', fontweight='bold')
        ax.set_xticks(ind + width / 2)
        ax.set_xticklabels(giornali)

        ax.legend(title='Commenti', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
        # Visualizzazione del grafico
        plt.xticks(rotation=0)
        plt.tight_layout()
        plt.savefig(f'IMAGES/pos-neg-{topic}-{titolo}.png')
        plt.show()
def create_hate_histogram(df,topic):
    for titolo in df['titolo'].unique():
        # Selezionare i dati relativi a un titolo specifico
        df_subset = df[df['titolo'] == titolo]
        # Creazione del grafico a barre con gruppi affiancati
        fig, ax = plt.subplots()

        # Raggruppamento per giornale e social e calcolo del numero di commenti
        commenti_per_giornale_social = df_subset.groupby(['giornale', 'social'])['hate_speech'].sum().unstack(
            fill_value=0)
        # Definizione dei colori per i social
        colori_social = {'Facebook': '#1877f2', 'Instagram': '#c32aa3', 'YouTube': '#ff0000'}

        # Creazione delle barre per ogni combinazione di giornale e social
        giornali = df_subset['giornale'].unique()
        socials = df_subset['social'].unique()
        n_giornali = len(giornali)
        n_socials = len(socials)
        width = 0.2
        space = 0.01  # Spazio tra le barre dello stesso gruppo
        total_width = width * n_socials + space * (n_socials - 1)  # Larghezza complessiva dei gruppi di barre
        ind = np.arange(n_giornali)

        for i, social in enumerate(commenti_per_giornale_social.columns):
            ax.bar(ind + i * (total_width + space) / n_socials + i * space / (n_socials - 1),
                   commenti_per_giornale_social[social], width=width, label=social, color=colori_social[social])

            # Aggiungi il numero di commenti sopra o vicino ogni barra
            for j, commenti in enumerate(commenti_per_giornale_social[social]):
                ax.annotate(f"{commenti}",
                            xy=(ind[j] + i * (total_width + space) / n_socials + i * space / (n_socials - 1), commenti),
                            ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', color='black',
                            fontsize=8)

        # Impostazione del titolo in grassetto
        ax.set_title(f'"{titolo}" - Topic: {topic}', fontweight='bold')
        ax.set_xlabel('Giornale', fontweight='bold')  # Impostazione dell'etichetta sull'asse x in grassetto
        ax.set_ylabel('Numero di commenti di odio',
                      fontweight='bold')  # Impostazione dell'etichetta sull'asse y in grassetto

        # Impostazione delle etichette della legenda
        ax.legend(title='Social', loc='upper left', bbox_to_anchor=(1, 1))

        # Impostazione delle etichette sull'asse x
        # Utilizza i dati del tuo dataset per le etichette
        ax.set_xticks([x + 0.2 for x in ind])
        ax.set_xticklabels(commenti_per_giornale_social.index)

        plt.xticks(rotation=0)

        # Impostazione del margine per garantire che l'intera legenda sia visibile
        plt.tight_layout()
        #Crea immagine
        plt.savefig(f'IMAGES/hate-{topic}-{titolo}.png')
        # Visualizzazione del grafico
        plt.show()
def create_pos_neg_pie(media_per_giornale, tipo_commento):
        for giornale, media_per_social in media_per_giornale.items():
            fig, axs = plt.subplots(1, len(media_per_social), figsize=(18, 6))
            fig.suptitle(f'Distribuzione dei commenti su {giornale} - {tipo_commento}', fontsize=16,fontweight='bold')

            for i, (social, media) in enumerate(media_per_social.items()):
                labels = ['Negativi', 'Positivi']
                sizes = [media['negativi'], media['positivi']]
                colors = ['orange', 'green']

                axs[i].pie(sizes, labels=None, colors=colors, autopct='%1.1f%%', startangle=140)
                axs[i].set_title(social, fontweight='bold')

            # Aggiungi la legenda una sola volta per immagine
            handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
            fig.legend(handles, labels, loc='center right')

            # Crea immagine
            plt.savefig(f'IMAGES/pie-pos-neg-{giornale}.png')
            plt.show()


def create_hate_speech_pie(media_per_giornale, tipo_commento):
        for giornale, media_per_social in media_per_giornale.items():
            fig, axs = plt.subplots(1, len(media_per_social), figsize=(18, 6))
            fig.suptitle(f'Distribuzione dei commenti su {giornale} - {tipo_commento}', fontsize=16,
                         fontweight='bold')

            for i, (social, media) in enumerate(media_per_social.items()):
                labels = ['Hate Speech', 'NON Hate Speech']
                sizes = [media['Hate_Speech'], media['NON_Hate_Speech']]
                colors = ['red', 'gray']

                axs[i].pie(sizes, labels=None, colors=colors, autopct='%1.1f%%', startangle=140)
                axs[i].set_title(f' {social}', fontweight='bold')

            # Aggiungi la legenda una sola volta per immagine
            handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in colors]
            fig.legend(handles, labels, loc='center right')
            # Crea immagine
            plt.savefig(f'IMAGES/pie-hate-{giornale}.png')
            plt.show()

# Leggi il file CSV
df = pd.read_csv('commenti_dataset_a.csv')
print(len(df))
hate_speech_mapping = {'no': False, 'inappropriato': True, 'offensivo': True, 'violento': True}
df['hate_speech_flag'] = df['hate_speech'].map(hate_speech_mapping)


# Raggruppa i dati per sentiment e hate_speech e conta il numero di commenti in ciascun gruppo
counts = df.groupby(['sentiment', 'hate_speech_flag']).size().reset_index(name='count')

# Filtra i dati per ottenere il numero di commenti che sono di odio + positivi e odio + negativi
hate_positive_count = counts[(counts['hate_speech_flag'] == True) & (counts['sentiment'] == 'positivo')]['count'].sum()
hate_negative_count = counts[(counts['hate_speech_flag'] == True) & (counts['sentiment'] == 'negativo')]['count'].sum()

print("Numero di commenti di odio positivi:", hate_positive_count)
print("Numero di commenti di odio negativi:", hate_negative_count)

# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]

hate_speech_mapping = {'no': False, 'inappropriato': True, 'offensivo': True, 'violento': True}
df['hate_speech_flag'] = df['hate_speech'].map(hate_speech_mapping)

# Raggruppa i dati per sentiment e hate_speech e conta il numero di commenti in ciascun gruppo
counts = df.groupby(['sentiment', 'hate_speech_flag']).size().reset_index(name='count')

# Filtra i dati per ottenere il numero di commenti che sono di odio + positivi e odio + negativi
hate_positive_count = counts[(counts['hate_speech_flag'] == True) & (counts['sentiment'] == 'positivo')]['count'].sum()
hate_negative_count = counts[(counts['hate_speech_flag'] == True) & (counts['sentiment'] == 'negativo')]['count'].sum()

print("Numero di commenti di odio positivi:", hate_positive_count)
print("Numero di commenti di odio negativi:", hate_negative_count)

#grafico
create_total_comments_category_histogram(df,commenti_hate_speech)
#grafico
create_topic_comments_category_histogram(df)

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
#create_count_histogram(commenti_per_notizia,"Istogramma - Numero di commenti per ogni notizia (suddivisi per giornale e social)","Notizia","Numero di commenti")


# Numero di commenti positivi e negativi per ogni notizia (titolo) per social
commenti_positivi_negativi_per_notizia = df.groupby(['titolo','giornale', 'social', 'sentiment']).size().unstack(fill_value=0).reset_index()
print("\nNumero di commenti positivi e negativi per ogni notizia:")
print(commenti_positivi_negativi_per_notizia)
#Excel
create_excel(commenti_positivi_negativi_per_notizia,"commenti_positivi_negativi_per_notizia","Numero di commenti positivi e negativi per ogni notizia")
#Grafico
#create_count_histogram(commenti_positivi_negativi_per_notizia,"Istogramma - Numero di commenti positivi e negativi per ogni notizia","Notizia","Numero di commenti")



# Numero di commenti di odio per ogni notizia suddivise per giornale e topic (titolo) per social
commenti_odio_per_notizia = commenti_hate_speech.groupby(['titolo', 'giornale','social']).size().reset_index(name='hate_speech')
# Stampa dei risultati
print("\nNumero di commenti odio per ogni notizia (suddivisi per giornale e social):")
print(commenti_odio_per_notizia)
#Excel
create_excel(commenti_odio_per_notizia,"commenti_odio_per_notizia","Numero di commenti odio per ogni notizia (suddivisi per giornale e social)")
#Grafico
#create_count_histogram(commenti_odio_per_notizia,"Istogramma - Numero di commenti odio per ogni notizia (suddivisi per giornale e social)","Notizia","Numero di commenti odio")



# Commenti negativi e positivi per ogni topic
commenti_per_topic = df.groupby(['topic','social','sentiment']).size().unstack(fill_value=0).reset_index()
print("\nCommenti negativi e positivi per ogni topic per social:")
print(commenti_per_topic)
#Excel
create_excel(commenti_per_topic,"commenti_per_topic","Commenti negativi e positivi per ogni topic per social")
#Grafico
#create_count_histogram(commenti_per_topic,"Istogramma - Commenti negativi e positivi per ogni topic per social","Topic","Numero di commenti")


# Commenti di odio per ogni topic
commenti_hS_per_topic = df.groupby(['topic','social','hate_speech']).size().unstack(fill_value=0).reset_index()
print("\nCommenti hate speech per ogni topic per social suddivisi per categoria di odio:")
print(commenti_hS_per_topic)
#Excel
create_excel(commenti_hS_per_topic,"commenti_hS_per_topic","Commenti hate speech per ogni topic per social suddivisi per categoria di odio")
#Grafico
#create_count_histogram(commenti_hS_per_topic,"Istogramma - Commenti hate speech per ogni topic per social suddivisi per categoria di odio","Topic","Numero di commenti hate speech")


# Conta il numero di commenti odio per ciascun topic
#num_commenti_hate_per_topic = commenti_hate_speech['topic'].value_counts()
num_commenti_hate_per_topic =commenti_hate_speech.groupby(['topic','social']).size().reset_index(name='num_hate_topic')
print("\nCommenti hate speech per ogni topic per social:  Mettere %")
print(num_commenti_hate_per_topic)
#Excel
create_excel(num_commenti_hate_per_topic,"num_commenti_hate_per_topic","Commenti hate speech per ogni topic per social")
#Grafico
#create_count_histogram(num_commenti_hate_per_topic,"Istogramma - Commenti hate speech per ogni topic per social","Topic","Percentuale di commenti hate speech")


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
create_negative_positive_histogram(commenti_positivi_negativi_per_notizia_cronaca,"CRONACA")


# Numero di commenti per ogni notizia suddivise per giornale e topic (titolo) per social TOPIC=CRONACA
commenti_per_notizia_cronaca = cronaca.groupby(['titolo', 'giornale','social']).size().reset_index(name='num_commenti')
# Stampa dei risultati
print("\nNumero di commenti per ogni notizia (suddivisi per giornale e social) (cronaca):")
print(commenti_per_notizia_cronaca)
#Excel
create_excel(commenti_per_notizia_cronaca,"commenti_per_notizia_cronaca","Numero di commenti per ogni notizia (suddivisi per giornale e social) (CRONACA)")
#Grafico
create_count_histogram(commenti_per_notizia_cronaca,"Social","Numero Commenti","CRONACA")


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
create_hate_histogram(commenti_odio_per_notizia_cronaca,"CRONACA")

#-------------------------CRONACA NERA-----------------------


cronaca_nera = df[df['topic'].str.lower() == 'cronaca nera']
# Numero di commenti per ogni notizia (titolo) per social TOPIC=CRONACA_NERA
commenti_positivi_negativi_per_notizia_cronaca_nera= cronaca_nera.groupby(['topic','titolo','giornale', 'social','sentiment']).size().unstack(fill_value=0).reset_index()
print("\nNumero di commenti positivi e negativi per ogni notizia (CRONACA NERA):")
print(commenti_positivi_negativi_per_notizia_cronaca_nera)
#Excel
create_excel(commenti_positivi_negativi_per_notizia_cronaca_nera,"commenti_positivi_negativi_per_notizia_cronaca_nera","Numero di commenti positivi e negativi per ogni notizia (CRONACA NERA)")
#Grafico
create_negative_positive_histogram(commenti_positivi_negativi_per_notizia_cronaca_nera,"CRONACA NERA")

# Numero di commenti per ogni notizia suddivise per giornale e topic (titolo) per social TOPIC=cronaca_nera
commenti_per_notizia_cronaca_nera = cronaca_nera.groupby(['titolo', 'giornale','social']).size().reset_index(name='num_commenti')
# Stampa dei risultati
print("\nNumero di commenti per ogni notizia (suddivisi per giornale e social) (cronaca_nera):")
print(commenti_per_notizia_cronaca_nera)
#Excel
create_excel(commenti_per_notizia_cronaca_nera,"commenti_per_notizia_cronaca_nera","Numero di commenti per ogni notizia (suddivisi per giornale e social) (CRONACA NERA)")
#Grafico
create_count_histogram(commenti_per_notizia_cronaca_nera,"Social","Numero Commenti","CRONACA NERA")


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
create_hate_histogram(commenti_odio_per_notizia_cronaca_nera,"CRONACA NERA")

#-------------------------POLITICA-----------------------

politica = df[df['topic'].str.lower() == 'politica']
# Numero di commenti per ogni notizia (titolo) per social TOPIC=politica
commenti_positivi_negativi_per_notizia_politica= politica.groupby(['topic','titolo','giornale', 'social','sentiment']).size().unstack(fill_value=0).reset_index()
print("\nNumero di commenti positivi e negativi per ogni notizia (POLITICA):")
print(commenti_positivi_negativi_per_notizia_politica)
#Excel
create_excel(commenti_positivi_negativi_per_notizia_politica,"commenti_positivi_negativi_per_notizia_politica","Numero di commenti positivi e negativi per ogni notizia (POLITICA)")
#Grafico
#create_negative_positive_histogram(commenti_positivi_negativi_per_notizia_politica,"POLITICA")

# Numero di commenti per ogni notizia suddivise per giornale e topic (titolo) per social TOPIC=politica
commenti_per_notizia_politica = politica.groupby(['titolo', 'giornale','social']).size().reset_index(name='num_commenti')
# Stampa dei risultati
print("\nNumero di commenti per ogni notizia (suddivisi per giornale e social) (politica):")
print(commenti_per_notizia_politica)
#Excel
create_excel(commenti_per_notizia_politica,"commenti_per_notizia_politica","Numero di commenti per ogni notizia (suddivisi per giornale e social) (POLITICA)")
#Grafico
create_count_histogram(commenti_per_notizia_politica,"Social","Numero Commenti","POLITICA")

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
create_hate_histogram(commenti_odio_per_notizia_politica,"POLITICA")

#--------------------------------------------------------------------------MEDIE------------------------------------------------------------------------------------------


# Numero di righe negative per ogni notizia/titolo e giornale per social
num_commenti_negativi_per_titolo_e_giornale = df[df['sentiment'] == 'negativo'].groupby(
    ['giornale', 'titolo', 'social']).size().reset_index(name='num_commenti_negativi')

# Calcola la media per ciascun giornale
media_negativi_per_giornale = num_commenti_negativi_per_titolo_e_giornale.groupby(['giornale', 'social'])[
    'num_commenti_negativi'].mean()

# Seleziona solo i commenti positivi
commenti_positivi = df[df['sentiment'] == 'positivo']

# Conta il numero di commenti positivi per ciascuna notizia e giornale per social
num_commenti_positivi_per_titolo_e_giornale = commenti_positivi.groupby(
    ['giornale', 'titolo', 'social']).size().reset_index(name='num_commenti_positivi')

# Calcola la media per ciascun giornale suddivisio per social
media_positivi_per_giornale = num_commenti_positivi_per_titolo_e_giornale.groupby(['giornale', 'social'])[
    'num_commenti_positivi'].mean()

# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech = df[df['hate_speech_flag'] == True]

# Numero di righe con commenti di hate_speech per ogni video, titolo e giornale
num_commenti_hate_speech_per_titolo_e_giornale = commenti_hate_speech.groupby(
    ['giornale', 'titolo', 'social']).size().reset_index(name='num_commenti_hate_speech')

# Calcola la media dei commenti di hate_speech per ciascun giornale
media_hate_speech_per_giornale = num_commenti_hate_speech_per_titolo_e_giornale.groupby(['giornale', 'social'])[
    'num_commenti_hate_speech'].mean()

commenti_non_hate_speech = df[df['hate_speech_flag'] == False]

# Numero di righe con commenti di hate_speech per ogni video, titolo e giornale
num_commenti_non_hate_speech_per_titolo_e_giornale = commenti_non_hate_speech.groupby(
    ['giornale', 'titolo', 'social']).size().reset_index(name='num_commenti_hate_speech')

# Calcola la media dei commenti di hate_speech per ciascun giornale
media_non_hate_speech_per_giornale = num_commenti_non_hate_speech_per_titolo_e_giornale.groupby(['giornale', 'social'])[
    'num_commenti_hate_speech'].mean()

# Visualizza il risultato
print(media_hate_speech_per_giornale)

for giornale, media_negativi in media_negativi_per_giornale.items():
    print(f'Giornale, Social: {giornale}, Media Commenti Negativi: {media_negativi:.2f}')

for giornale, media_positivi in media_positivi_per_giornale.items():
    print(f'Giornale, Social: {giornale}, Media Commenti Positivi: {media_positivi:.2f}')

for giornale, media_hate_speech in media_hate_speech_per_giornale.items():
    print(f'Giornale, Social: {giornale}, Media Commenti Hate Speech: {media_hate_speech:.2f}')

for giornale, media_non_hate_speech in media_non_hate_speech_per_giornale.items():
    print(f'Giornale, Social: {giornale}, Media Commenti NON Hate Speech: {media_non_hate_speech:.2f}')


# Crea un dizionario vuoto per memorizzare le medie
medie_per_giornale = {}

# Itera attraverso le medie dei commenti negativi
for (giornale_social, media_negativi) in media_negativi_per_giornale.items():
        if giornale_social[0] not in medie_per_giornale:
            medie_per_giornale[giornale_social[0]] = {}
        if giornale_social[1] not in medie_per_giornale[giornale_social[0]]:
            medie_per_giornale[giornale_social[0]][giornale_social[1]] = {}
        medie_per_giornale[giornale_social[0]][giornale_social[1]]['negativi'] = media_negativi

# Itera attraverso le medie dei commenti positivi
for (giornale_social, media_positivi) in media_positivi_per_giornale.items():
        if giornale_social[0] not in medie_per_giornale:
            medie_per_giornale[giornale_social[0]] = {}
        if giornale_social[1] not in medie_per_giornale[giornale_social[0]]:
            medie_per_giornale[giornale_social[0]][giornale_social[1]] = {}
        medie_per_giornale[giornale_social[0]][giornale_social[1]]['positivi'] = media_positivi

# Stampare la struttura del dizionario
print(medie_per_giornale)
# Crea grafico
create_pos_neg_pie(medie_per_giornale,"Commenti Positivi e Negativi" )

media_hate_per_giornale = {}

# Itera attraverso le medie dei commenti positivi
for (giornale_social, media_hate_speech) in media_hate_speech_per_giornale.items():
        if giornale_social[0] not in media_hate_per_giornale:
            media_hate_per_giornale[giornale_social[0]] = {}
        if giornale_social[1] not in media_hate_per_giornale[giornale_social[0]]:
            media_hate_per_giornale[giornale_social[0]][giornale_social[1]] = {}
        media_hate_per_giornale[giornale_social[0]][giornale_social[1]]['Hate_Speech'] = media_hate_speech

# Itera attraverso le medie dei commenti positivi
for (giornale_social, media_non_hate_speech) in media_non_hate_speech_per_giornale.items():
        if giornale_social[0] not in media_hate_per_giornale:
            media_hate_per_giornale[giornale_social[0]] = {}
        if giornale_social[1] not in media_hate_per_giornale[giornale_social[0]]:
            media_hate_per_giornale[giornale_social[0]][giornale_social[1]] = {}
        media_hate_per_giornale[giornale_social[0]][giornale_social[1]]['NON_Hate_Speech'] = media_non_hate_speech


# Stampare la struttura del dizionario
print(media_hate_per_giornale)
#Crea grafico
create_hate_speech_pie(media_hate_per_giornale, "Commenti Hate Speech")


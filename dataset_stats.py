import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt



hline = ' ------------------------ '


def crea_grafici_a_torta2(media_per_giornale, tipo_commento):
    for giornale, media_per_social in media_per_giornale.items():
        fig, axs = plt.subplots(1, len(media_per_social), figsize=(18, 6))
        fig.suptitle(f'Distribuzione dei commenti su {giornale} - {tipo_commento}', fontsize=16)

        for i, (social, media) in enumerate(media_per_social.items()):
            labels = ['Hate_Speech', 'NON_Hate_Speech']
            sizes = [media['Hate_Speech'], media['NON_Hate_Speech']]
            colors = ['orange', 'gray']

            axs[i].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            axs[i].set_title(social)

        plt.show()

def print_dataset_stats(csv_file):

    # Carica il file CSV in un DataFrame
    df = pd.read_csv(csv_file)
    hate_speech_mapping = {'no': False, 'inappropriato': True, 'offensivo': True, 'violento': True}
    df['hate_speech_flag'] = df['hate_speech'].map(hate_speech_mapping)


    print(len(df))
    # STATS: notizia-topic
    selected_df = df[['titolo','topic']]
    unique_df = selected_df.drop_duplicates()
    df_sorted = unique_df.sort_values(by='topic')
    print(df_sorted)

    print(hline)

    # Crea una tabella pivot
    pivot_table = pd.pivot_table(df, 
                                index=['titolo', 'topic', 'giornale'], 
                                columns='social', 
                                values='commento', 
                                aggfunc='count', 
                                fill_value=0)

    # Resetta l'indice
    pivot_table = pivot_table.reset_index()

    # Rinomina le colonne
    pivot_table.columns.name = None

    # Rinomina le colonne dei social
    pivot_table.rename(columns={'facebook': 'Facebook',
                                'instagram': 'Instagram',
                                'youtube': 'Youtube'}, 
                    inplace=True)
    print(pivot_table)

    print(hline)

    commenti_per_topic = df.groupby(['topic', 'social', 'sentiment']).size().unstack(fill_value=0).reset_index()
    commenti_per_topic['Total'] = commenti_per_topic['negativo'] + commenti_per_topic['positivo']
    commenti_per_topic['% positivo'] = ((commenti_per_topic['positivo'] / commenti_per_topic['Total']) * 100).round(1)
    commenti_per_topic['% negativo'] = ((commenti_per_topic['negativo'] / commenti_per_topic['Total']) * 100).round(1)
    print("\nCommenti negativi e positivi per ogni topic per social:")

    print(commenti_per_topic)

    print(hline)


    # Filtra il DataFrame per includere solo i commenti negativi
    commenti_negativi = df[df['sentiment'] == 'negativo']

    hate_speech_per_topic = commenti_negativi.groupby(['topic', 'social', 'hate_speech']).size().unstack(fill_value=0).reset_index()
    hate_speech_per_topic['Total'] = hate_speech_per_topic['no'] + hate_speech_per_topic['inappropriato'] + hate_speech_per_topic['offensivo'] + hate_speech_per_topic['violento']

    hate_speech_per_topic['% no'] = ((hate_speech_per_topic['no'] / hate_speech_per_topic['Total']) * 100).round(1)
    hate_speech_per_topic['% inappropriato'] = ((hate_speech_per_topic['inappropriato'] / hate_speech_per_topic['Total']) * 100).round(1)
    hate_speech_per_topic['% offensivo'] = ((hate_speech_per_topic['offensivo'] / hate_speech_per_topic['Total']) * 100).round(1)
    hate_speech_per_topic['% violento'] = ((hate_speech_per_topic['violento'] / hate_speech_per_topic['Total']) * 100).round(1)

    print("\nPercentuali di hate speech per ogni topic per social:")
    print(hate_speech_per_topic)

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

    for giornale, media_negativi in media_negativi_per_giornale.items():
        print(f'Giornale, Social: {giornale}, Media Commenti Negativi: {media_negativi:.2f}')

    for giornale, media_positivi in media_positivi_per_giornale.items():
        print(f'Giornale, Social: {giornale}, Media Commenti Positivi: {media_positivi:.2f}')

    for giornale, media_hate_speech in media_hate_speech_per_giornale.items():
        print(f'Giornale, Social: {giornale}, Media Commenti Hate Speech: {media_hate_speech:.2f}')

    for giornale, media_non_hate_speech in media_non_hate_speech_per_giornale.items():
        print(f'Giornale, Social: {giornale}, Media Commenti NON Hate Speech: {media_non_hate_speech:.2f}')

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

            plt.show()

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

    create_hate_speech_pie(media_hate_per_giornale, "Commenti Hate Speech")


def main():
    dataset_file = 'commenti_dataset_a.csv'

    print_dataset_stats(dataset_file)
    fix(dataset_file)

# Per normalizzare il dataset in caso di errori tra colonne
def fix(file_path):
    '''
    df = pd.read_csv(file_path)
    filtered_rows = df['giornale'] != 'Il Fatto Quotidiano'
    df = df[filtered_rows]
    df.to_csv(file_path, index=False)  
    '''

    df = pd.read_csv(file_path)
    filtered_rows = df['titolo'] == 'L\'implosione del sottomarino Titan'
    df.loc[filtered_rows, 'topic'] = 'CRONACA NERA'
    df.to_csv(file_path, index=False)


if __name__ == '__main__':
    main()
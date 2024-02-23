import pandas as pd


hline = ' ------------------------ '

def print_dataset_stats(csv_file):

    # Carica il file CSV in un DataFrame
    df = pd.read_csv(csv_file)
    hate_speech_mapping = {'no': False, 'inappropriato': True, 'offensivo': True, 'violento': True}
    df['hate_speech_flag'] = df['hate_speech'].map(hate_speech_mapping)

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
    commenti_hate_speech = df[df['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]

    # Numero di righe con commenti di hate_speech per ogni video, titolo e giornale
    num_commenti_hate_speech_per_titolo_e_giornale = commenti_hate_speech.groupby(
        ['giornale', 'titolo', 'social']).size().reset_index(name='num_commenti_hate_speech')

    # Calcola la media dei commenti di hate_speech per ciascun giornale
    media_hate_speech_per_giornale = num_commenti_hate_speech_per_titolo_e_giornale.groupby(['giornale', 'social'])[
        'num_commenti_hate_speech'].mean()

    # Visualizza il risultato
    print(media_hate_speech_per_giornale)

    for giornale, media_negativi in media_negativi_per_giornale.items():
        print(f'Giornale, Social: {giornale}, Media Commenti Negativi: {media_negativi:.2f}')

    for giornale, media_positivi in media_positivi_per_giornale.items():
        print(f'Giornale, Social: {giornale}, Media Commenti Positivi: {media_positivi:.2f}')

    for giornale, media_hate_speech in media_hate_speech_per_giornale.items():
        print(f'Giornale, Social: {giornale}, Media Commenti Hate Speech: {media_hate_speech:.2f}')



    # Raggruppa i dati per sentiment e hate_speech e conta il numero di commenti in ciascun gruppo
    counts = df.groupby(['sentiment', 'hate_speech_flag']).size().reset_index(name='count')

    # Filtra i dati per ottenere il numero di commenti che sono di odio + positivi e odio + negativi
    hate_positive_count = counts[(counts['hate_speech_flag'] == True) & (counts['sentiment'] == 'positivo')]['count'].sum()
    hate_negative_count = counts[(counts['hate_speech_flag'] == True) & (counts['sentiment'] == 'negativo')]['count'].sum()

    print("Numero di commenti di odio positivi:", hate_positive_count)
    print("Numero di commenti di odio negativi:", hate_negative_count)


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
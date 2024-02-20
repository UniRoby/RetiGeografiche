import pandas as pd


hline = ' ------------------------ '

def print_dataset_stats(csv_file):

    # Carica il file CSV in un DataFrame
    df = pd.read_csv(csv_file)

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
    


def main():
    dataset_file = 'commenti_dataset.csv'
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
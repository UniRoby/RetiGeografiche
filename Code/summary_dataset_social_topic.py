import pandas as pd


def main():
    # Lettura del file CSV
    df = pd.read_csv('commenti_dataset_a.csv')

    # Mappatura dei valori di hate speech
    hate_speech_mapping = {'no': False, 'inappropriato': True, 'offensivo': True, 'violento': True}
    df['hate_speech_flag'] = df['hate_speech'].map(hate_speech_mapping)

    # Raggruppamento dei commenti per 'topic', 'social', 'sentiment' e calcolo del numero di commenti positivi e negativi
    grouped_comments = df.groupby(['topic', 'social', 'sentiment']).size().unstack(fill_value=0).reset_index()

    # Rinominiamo le colonne 'positivo' e 'negativo'
    grouped_comments.rename(columns={'positivo': 'POSITIVI', 'negativo': 'NEGATIVI'}, inplace=True)

    # Raggruppamento dei commenti per 'topic', 'social', e 'hate_speech' e calcolo del numero di commenti di hate speech
    hate_speech_comments = df.groupby(['topic', 'social', 'hate_speech_flag']).size().unstack(fill_value=0).reset_index()

    hate_speech_comments.rename(columns={True: 'HATE', False: 'NO_HATE'}, inplace=True)


    final_table = pd.merge(grouped_comments, hate_speech_comments[['topic', 'social', 'HATE']], on=['topic', 'social'], how='left')

    final_table['TOTALE'] = final_table['POSITIVI'] + final_table['NEGATIVI']

    final_table['%POSITIVI'] = ((final_table['POSITIVI'] / final_table['TOTALE']) * 100).round(1)
    final_table['%NEGATIVI'] = ((final_table['NEGATIVI'] / final_table['TOTALE']) * 100).round(1)
    final_table['%HATE'] = ((final_table['HATE'] / final_table['TOTALE']) * 100).round(1)

    print(final_table)

if __name__ == '__main__':
    main()

import pandas as pd
import matplotlib.pyplot as plt

def fix(csv_file):
     # Carica il file CSV in un DataFrame
    df = pd.read_csv(csv_file)

    # Converte il campo "social" in minuscolo
    df['social'] = df['social'].str.lower()

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

    # Visualizza la tabella pivot
    print(pivot_table)

    # Verifica e duplica i commenti
    for index, row in pivot_table.iterrows():
        for social in ['Facebook', 'Instagram', 'Youtube']:
            if 80 <= row[social] < 100:
                # Trova un altro commento per la stessa notizia da un'altra testata
                other_comment = df[(df['titolo'] == row['titolo']) & (df['topic'] == row['topic']) & (df['giornale'] != row['giornale'])].sample(n=1)['commento'].values[0]
                
                # Calcola quante occorrenze sono necessarie per raggiungere 100
                num_to_add = 100 - row[social]
                # Duplica il commento il numero di volte necessario
                for _ in range(num_to_add):
                    df = df.append({'social': social.lower(), 'giornale': row['giornale'], 'titolo': row['titolo'], 'commento': other_comment, 'topic': row['topic']}, ignore_index=True)

    # Salva il DataFrame in un nuovo file CSV
    df.to_csv('test.csv', index=False)  # Specifica il nome del file che desideri


def create_tab_stats(csv_file):

    # Carica il file CSV in un DataFrame
    df = pd.read_csv(csv_file)

   # Converte il campo "social" in minuscolo
    df['social'] = df['social'].str.lower()

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

    # Visualizza la tabella pivot
    print(pivot_table)

def main():
    
    file = 'commenti_dataset_a.csv'

    create_tab_stats(file)
    #fix(file)

if __name__=='__main__':
    main()
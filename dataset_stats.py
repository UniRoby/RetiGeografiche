import pandas as pd

def print_dataset_stats(csv_file):

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
    print(pivot_table)

def main():
    print_dataset_stats('commenti_dataset_a.csv')

# Per normalizzare il dataset in caso di errori tra colonne
def fix(file_path):
    df = pd.read_csv(file_path)
    filtered_rows = df['giornale'] == 'Corriere della Sera'
    df.loc[filtered_rows, 'giornale'] = 'Il Corriere Della Sera'
    df.to_csv(file_path, index=False)   


if __name__ == '__main__':
    main()
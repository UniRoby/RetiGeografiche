import pandas as pd

def print_dataset_stats(file_path):
    df = pd.read_csv(file_path)

    conteggi_commenti = df.groupby(['titolo', 'giornale', 'topic', 'social']).size().reset_index(name='Numero di Commenti')

    print(conteggi_commenti.to_string(index=False))

def main():
    print_dataset_stats('commenti_dataset_a.csv')


'''

def fix(file_path):
    df = pd.read_csv(file_path)
    filtered_rows = df['giornale'] == 'Corriere Della Sera'
    df.loc[filtered_rows, 'giornale'] = 'Il Corriere Della Sera'
    df.to_csv(file_path, index=False)   
'''

if __name__ == '__main__':
    main()
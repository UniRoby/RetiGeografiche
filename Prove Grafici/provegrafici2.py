import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("commenti_dataset_r.csv")
cronaca = df[df['topic'].str.lower() == 'cronaca']
df= cronaca.groupby(['topic','titolo','giornale', 'social','sentiment']).size().unstack(fill_value=0).reset_index()

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
    ax.set_xlabel('Giornale', fontweight='bold')
    ax.set_ylabel('Numero di commenti', fontweight='bold')
    ax.set_title(f'"{titolo}" - Topic: CRONACA', fontweight='bold')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(giornali)

    ax.legend(title='Commenti', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)
    # Visualizzazione del grafico
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Definizione del dataset
df = pd.read_csv("/Users/roby/PycharmProjects/RetiGeografiche/commenti_dataset_r.csv")
cronaca = df[df['topic'].str.lower() == 'cronaca']
# Filtra solo i commenti con hate_speech nelle categorie 'inappropriato', 'offensivo' e 'violento'
commenti_hate_speech_cronaca = cronaca[cronaca['hate_speech'].isin(['inappropriato', 'offensivo', 'violento'])]

# Numero di commenti di odio per ogni notizia suddivise per giornale e topic (titolo) per social
df = commenti_hate_speech_cronaca.groupby(['titolo', 'giornale', 'social']).size().reset_index(name='hate_speech')

# Definizione dei colori per i social
colori_social = {'Facebook': 'blue', 'Instagram': 'pink', 'YouTube': 'red'}

for titolo in df['titolo'].unique():
    # Selezionare i dati relativi a un titolo specifico
    df_subset = df[df['titolo'] == titolo]
    # Creazione del grafico a barre con gruppi affiancati
    fig, ax = plt.subplots()

    # Raggruppamento per giornale e social e calcolo del numero di commenti
    commenti_per_giornale_social = df_subset.groupby(['giornale', 'social'])['hate_speech'].sum().unstack(fill_value=0)

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
        #ax.bar([x + width * i for x in ind], commenti_per_giornale_social[social], width=width, label=social, color=colori_social[social])
        ax.bar(ind + i * (total_width + space) / n_socials + i * space / (n_socials - 1),commenti_per_giornale_social[social] , width=width, label=social, color=colori_social[social])

    # Impostazione del titolo in grassetto
    ax.set_title(f'"{titolo}" - Topic: Cronaca', fontweight='bold')
    ax.set_xlabel('Giornale', fontweight='bold')  # Impostazione dell'etichetta sull'asse x in grassetto
    ax.set_ylabel('Numero di commenti di odio', fontweight='bold')  # Impostazione dell'etichetta sull'asse y in grassetto

    # Impostazione delle etichette della legenda
    ax.legend(title='Social', loc='upper left', bbox_to_anchor=(1, 1))

    # Impostazione delle etichette sull'asse x
    # Utilizza i dati del tuo dataset per le etichette
    ax.set_xticks([x + 0.2 for x in ind])
    ax.set_xticklabels(commenti_per_giornale_social.index)

    plt.xticks(rotation=0)

    # Impostazione del margine per garantire che l'intera legenda sia visibile
    plt.tight_layout()

    # Visualizzazione del grafico
    plt.show()

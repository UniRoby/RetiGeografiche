import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Creazione del DataFrame dai dati forniti
data = {
    'Titolo': ['Alluvioni Emilia Romagna'] * 9,
    'Social': ['Facebook', 'Instagram', 'YouTube'] * 3,
    'Giornale': ['FanPage'] * 3 + ['Il Corriere Della Sera'] * 3 + ['La Repubblica'] * 3,
    'Positivi': [96, 53, 67, 72, 65, 82, 53, 72, 77],
    'Negativi': [18, 14, 31, 35, 6, 19, 9, 13, 16]
}

df = pd.DataFrame(data)

# Raggruppamento per giornale e social
grouped_df = df.groupby(['Giornale', 'Social']).sum()

# Estrazione dei valori per le etichette sull'asse x e i valori dei commenti
giornali = df['Giornale'].unique()
socials = df['Social'].unique()
n_giornali = len(giornali)
n_socials = len(socials)
width = 0.2
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
        positivi.append(grouped_df.loc[giornale, social]['Positivi'])
        negativi.append(grouped_df.loc[giornale, social]['Negativi'])

    ax.bar(ind + i * width, negativi, width, label=f'{social} - Negativi', color=colors[social][0])
    ax.bar(ind + i * width, positivi, width, label=f'{social} - Positivi', bottom=negativi, color=colors[social][1])

# Impostazione delle etichette sugli assi
ax.set_xlabel('Giornale', fontweight='bold')
ax.set_ylabel('Numero di commenti', fontweight='bold')
ax.set_title('Commenti positivi e negativi per giornale e social', fontweight='bold')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(giornali)

ax.legend(title='Commenti', loc='upper center', bbox_to_anchor=(0.5, -0.15),ncol=3)
# Visualizzazione del grafico
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

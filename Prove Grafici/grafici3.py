import pandas as pd
import matplotlib.pyplot as plt

# Creazione del DataFrame dai dati forniti
data = {
    'Titolo': ['Alluvioni Emilia Romagna'] * 9,
    'Social': ['FanPage'] * 3 + ['Il Corriere Della Sera'] * 3 + ['La Repubblica'] * 3,
    'Giornale': ['Facebook', 'Instagram', 'YouTube'] * 3,
    'Commenti': [114, 67, 98, 107, 71, 101, 62, 85, 93]
}

df = pd.DataFrame(data)

# Creazione del grafico a barre con gruppi affiancati
fig, ax = plt.subplots()

# Raggruppamento per social e giornale e calcolo del numero di commenti
commenti_per_social_giornale = df.groupby(['Social', 'Giornale'])['Commenti'].sum().unstack(fill_value=0)

# Calcolo delle posizioni dei gruppi di barre
ind = range(len(commenti_per_social_giornale.index))

# Creazione delle barre per ogni combinazione di social e giornale
width = 0.2
for i, col in enumerate(commenti_per_social_giornale.columns):
    ax.bar([x + width * i for x in ind], commenti_per_social_giornale[col], width=width, label=col)

# Impostazione del titolo in grassetto
ax.set_title(f'"{df["Titolo"].iloc[0]}" - Topic: Cronaca', fontweight='bold')
ax.set_xlabel('Giornale', fontweight='bold')  # Impostazione dell'etichetta sull'asse x in grassetto
ax.set_ylabel('Numero di commenti', fontweight='bold')  # Impostazione dell'etichetta sull'asse y in grassetto

# Impostazione delle etichette della legenda
ax.legend(title='Social', loc='upper left', bbox_to_anchor=(1, 1))

# Impostazione delle etichette sull'asse x
ax.set_xticks([x + 0.2 for x in ind])
ax.set_xticklabels(commenti_per_social_giornale.index)

plt.xticks(rotation=0)

# Impostazione del margine per garantire che l'intera legenda sia visibile
plt.tight_layout()

# Visualizzazione del grafico
plt.show()


# Impostazione del margine per garantire che l'intera legenda sia visibile
plt.tight_layout()

# Visualizzazione del grafico
plt.show()
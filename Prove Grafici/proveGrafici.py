import pandas as pd
import matplotlib.pyplot as plt

# Creazione del DataFrame dai dati forniti
data = {
    'Titolo': ['Alluvioni Emilia Romagna'] * 9,
    'Social': ['Facebook', 'Instagram', 'YouTube'] * 3,
    'Giornale': ['FanPage'] * 3 + ['Il Corriere Della Sera'] * 3 + ['La Repubblica'] * 3,
    'Positivi': [96, 53, 67, 72, 65, 82, 53, 72, 77],
    'Negativi': [18, 14, 31, 35, 6, 19, 9, 13, 16]
}

df = pd.DataFrame(data)

# Raggruppamento per social e giornale e calcolo del numero di commenti
grouped_data = df.groupby(['Social', 'Giornale']).sum().unstack()

# Creazione del grafico
fig, ax = plt.subplots()

# Etichettatura degli assi e titolo del grafico
ax.set_ylabel('Numero di commenti')
ax.set_xlabel('Social')
ax.set_title('Alluvioni Emilia Romagna - CRONACA')

# larghezza delle barre
width = 0.35

# Creazione delle barre sovrapposte per ogni giornale
for giornale in grouped_data.columns.get_level_values('Giornale'):
    ax.bar(grouped_data.index, grouped_data[('Negativi', giornale)], width, label=f'{giornale} - Negativi', bottom=grouped_data[('Positivi', giornale)], alpha=0.5)
    ax.bar(grouped_data.index, grouped_data[('Positivi', giornale)], width, label=f'{giornale} - Positivi')

# Aggiunta della legenda
ax.legend()

plt.show()





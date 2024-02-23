import matplotlib.pyplot as plt

# Dati relativi ai commenti per ogni giornale e social
dati = {
    'FanPage': {
        'Facebook': {'negativi': 75.83, 'positivi': 22.25, 'hate_speech': 10.25},
        'Instagram': {'negativi': 82.00, 'positivi': 17.67, 'hate_speech': 16.58},
        'YouTube': {'negativi': 82.58, 'positivi': 22.67, 'hate_speech': 7.17}
    },
    'Il Corriere Della Sera': {
        'Facebook': {'negativi': 73.92, 'positivi': 24.58, 'hate_speech': 7.25},
        'Instagram': {'negativi': 82.25, 'positivi': 14.42, 'hate_speech': 14.17},
        'YouTube': {'negativi': 81.08, 'positivi': 20.17, 'hate_speech': 7.33}
    },
    'La Repubblica': {
        'Facebook': {'negativi': 76.25, 'positivi': 20.67, 'hate_speech': 14.30},
        'Instagram': {'negativi': 81.67, 'positivi': 14.50, 'hate_speech': 18.58},
        'YouTube': {'negativi': 80.00, 'positivi': 22.75, 'hate_speech': 7.58}
    }
}

# Creazione di un'immagine contenente tre grafici a torta per ogni giornale
for giornale, social_dati in dati.items():
    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f'Distribuzione dei commenti su {giornale}', fontsize=16)

    for i, (social, commenti) in enumerate(social_dati.items()):
        labels = ['Negativi', 'Positivi', 'Hate Speech']
        sizes = [commenti['negativi'], commenti['positivi'], commenti['hate_speech']]
        colors = ['red', 'green', 'gray']

        axs[i].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        axs[i].set_title(social)

    plt.show()

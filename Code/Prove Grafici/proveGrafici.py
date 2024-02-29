import pandas as pd
import matplotlib.pyplot as plt


# Funzione per creare i grafici a torta
def crea_grafici_a_torta(media_per_giornale, tipo_commento):
    for giornale, media_per_social in media_per_giornale.items():
        fig, axs = plt.subplots(1, len(media_per_social), figsize=(18, 6))
        fig.suptitle(f'Distribuzione dei commenti su {giornale} - {tipo_commento}', fontsize=16)

        for i, (social, media) in enumerate(media_per_social.items()):
            labels = ['Negativi', 'Positivi']
            sizes = [media['negativi'], media['positivi']]
            colors = ['red', 'green']

            axs[i].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            axs[i].set_title(social)

        plt.show()


# Esempio di dati delle medie per ogni giornale e social (sostituire con i tuoi dati effettivi)
media_negativi_per_giornale = {
    'FanPage': {'Facebook': {'negativi': 75.83, 'positivi': 22.25}, 'Instagram': {'negativi': 82.00, 'positivi': 17.67},'YouTube': {'negativi': 82.58, 'positivi': 22.67}},
    'Il Corriere Della Sera': {'Facebook': {'negativi': 73.92, 'positivi': 24.58},
                               'Instagram': {'negativi': 82.25, 'positivi': 14.42},
                               'YouTube': {'negativi': 81.08, 'positivi': 20.17}},
    'La Repubblica': {'Facebook': {'negativi': 76.25, 'positivi': 20.67},
                      'Instagram': {'negativi': 81.67, 'positivi': 14.50},
                      'YouTube': {'negativi': 80.00, 'positivi': 22.75}}
}

# Chiamata alla funzione per creare i grafici per i commenti positivi e negativi
crea_grafici_a_torta(media_negativi_per_giornale, tipo_commento='commenti')

# Esempio di dati delle medie per i commenti di hate speech per ogni giornale e social (sostituire con i tuoi dati effettivi)
media_hate_speech_per_giornale = {
    'FanPage': {'Facebook': {'negativi': 10.25, 'positivi': 5.75}, 'Instagram': {'negativi': 16.58, 'positivi': 8.42},
                'YouTube': {'negativi': 7.17, 'positivi': 13.83}},
    'Il Corriere Della Sera': {'Facebook': {'negativi': 7.25, 'positivi': 8.75},
                               'Instagram': {'negativi': 14.17, 'positivi': 12.08},
                               'YouTube': {'negativi': 7.33, 'positivi': 12.67}},
    'La Repubblica': {'Facebook': {'negativi': 14.30, 'positivi': 5.70},
                      'Instagram': {'negativi': 18.58, 'positivi': 1.42},
                      'YouTube': {'negativi': 7.58, 'positivi': 10.42}}
}

# Chiamata alla funzione per creare i grafici per i commenti di hate speech con flag True e False
crea_grafici_a_torta(media_hate_speech_per_giornale, tipo_commento='hate_speech')



import pandas as pd
import matplotlib.pyplot as plt

def crea_grafici_a_torta2(media_per_giornale, tipo_commento):
    for giornale, media_per_social in media_per_giornale.items():
        fig, axs = plt.subplots(1, len(media_per_social), figsize=(18, 6))
        fig.suptitle(f'Distribuzione dei commenti su {giornale} - {tipo_commento}', fontsize=16)

        for i, (social, media) in enumerate(media_per_social.items()):
            labels = ['Hate_Speech', 'NON_Hate_Speech']
            sizes = [media['Hate_Speech'], media['NON_Hate_Speech']]
            colors = ['orange', 'gray']

            axs[i].pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            axs[i].set_title(social)

        plt.show()


media_hate_speech_per_giornale = {
    'FanPage': {'Facebook': {'Hate_Speech': 10.25, 'NON_Hate_Speech': 5.75},
                'Instagram': {'Hate_Speech': 16.58, 'NON_Hate_Speech': 8.42},
                'YouTube': {'Hate_Speech': 7.17, 'NON_Hate_Speech': 13.83}},
    'Il Corriere Della Sera': {'Facebook': {'Hate_Speech': 7.25, 'NON_Hate_Speech': 8.75},
                                'Instagram': {'Hate_Speech': 14.17, 'NON_Hate_Speech': 12.08},
                                'YouTube': {'Hate_Speech': 7.33, 'NON_Hate_Speech': 12.67}},
    'La Repubblica': {'Facebook': {'Hate_Speech': 14.30, 'NON_Hate_Speech': 5.70},
                        'Instagram': {'Hate_Speech': 18.58, 'NON_Hate_Speech': 1.42},
                        'YouTube': {'Hate_Speech': 7.58, 'NON_Hate_Speech': 10.42}}
}


# Creazione dei grafici per i commenti di hate speech con flag True
crea_grafici_a_torta2(media_hate_speech_per_giornale, tipo_commento='Hate Speech True')






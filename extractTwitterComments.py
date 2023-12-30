import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import commentsDataset as cd

def twitterComments():
    # Leggi il nuovo dataset
    df = pd.read_csv('TW_REPLY_Corriere_1740760935445262664_27.csv')

    # ottieni l'autore del post
    commenti= df["full_text"].tolist()

    listComments=[]

    for i,comment in enumerate(commenti):
        listComments.append(cd.removeSymbolsAndEmoticons(comment))


    canale= input("Pagina (autore): ")
    titolo= input("Post (titolo): ")
    topic= input("Topic: ")

    cd.createOrUpdateDataset(listComments, canale, titolo, topic,"Twitter")



twitterComments()
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import commentsDataset as cd

def IgComments():
    # Leggi il nuovo dataset
    df = pd.read_csv('IG/ig.csv')

    # ottieni l'autore del post
    commenti= df["Content"].tolist()

    listComments=[]

    for i,comment in enumerate(commenti):
        listComments.append(cd.removeSymbolsAndEmoticons(comment))

    print(f"Numero commenti estratti: {len(listComments)}")
    canale= input("Pagina (autore): ")
    titolo= input("Post (titolo): ")
    topic= input("Topic: ")

    cd.createOrUpdateDataset(listComments, canale, titolo, topic,"Instagram")


IgComments()
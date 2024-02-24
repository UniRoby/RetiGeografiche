import re
import pandas as pd
from feel_it import  SentimentClassifier
from transformers import pipeline
import os


#rimuovi emoji e altri simboli
def removeSymbolsAndEmoticons(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F700-\U0001F77F"  # alchemical symbols
                               u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
                               u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
                               u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                               u"\U0001FA00-\U0001FA6F"  # Chess Symbols
                               u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
                               u"\U00002702-\U000027B0"  # Dingbat Symbols
                               u"\U000024C2-\U0001F251"  # Enclosed Characters
                               "]+", flags=re.UNICODE)

    new_text = emoji_pattern.sub(r'', text)

    # Rimuovi testo tra "@" e lo spazio successivo

    at_pattern = re.compile(r'[\s\u200B\u00A0]*@.*?[\s\u200B\u00A0]')
    #rimuovi eventuali link nei commenti
    link_pattern = re.compile(r'https?://\S+|www\.\S+')
    new_text = at_pattern.sub(r'', new_text)
    new_text=link_pattern.sub('',new_text)
    new_text= new_text.replace('"', '')

    return new_text

def getTarget(comment):

    sentiment_classifier = SentimentClassifier()
    sentiment=sentiment_classifier.predict([comment])
    match sentiment[0]:
        case 'negative': return 'negativo'
        case 'positive': return 'positivo'

def getSpeechDet(comment):

    pipe = pipeline("text-classification", model="IMSyPP/hate_speech_it")
    hate_speech=pipe(comment)
    match hate_speech[0]['label']:
        case 'LABEL_0': return 'no'
        case 'LABEL_1': return 'inappropriato'
        case 'LABEL_2': return 'offensivo'
        case 'LABEL_3': return 'violento'


def createOrUpdateDataset(comments, giornale, titolo,topic,social):


    comment_data = [{"social": social,"giornale": giornale, "titolo": titolo, "commento": comment,"topic": topic, "sentiment": getTarget(comment), "hate_speech": getSpeechDet(comment)} for comment in comments if len(comment) > 0]

    #Creazione di un DataFrame pandas
    df = pd.DataFrame(comment_data)

    # Nome del file CSV
    csv_filename = 'commenti_dataset_a.csv'

    # Se il file CSV esiste già, apri il file e aggiungi le nuove righe
    if os.path.exists(csv_filename):
        existing_df = pd.read_csv(csv_filename)
        updated_df = pd.concat([existing_df, df], ignore_index=False)
        updated_df.to_csv(csv_filename, index=False)
    else:
        # Se il file CSV non esiste, crea un nuovo file
        df.to_csv(csv_filename, index=False)






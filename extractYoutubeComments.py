import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import commentsDataset as cd
from itertools import islice
from youtube_comment_downloader import *

import pandas as pd

from pytube import YouTube



def extractVideoComments(youtubeUrl,numComments):
    downloader = YoutubeCommentDownloader()
    comments = downloader.get_comments_from_url(youtubeUrl, sort_by=SORT_BY_POPULAR)
    listComments=[]

    for comment in islice(comments, numComments):

        listComments.append(comment["text"])
    listCommentsCustom=[]
    for comment in listComments:
        listCommentsCustom.append(cd.removeSymbolsAndEmoticons(comment))


    return listCommentsCustom


def ytComments():

    videoUrl = input("inserisci l'url del video di YouTube: ")
    topic = input("Topic: ")
    titolo = input("Titolo): ")
    numCommenti = 100
    link = videoUrl
    yt = YouTube(link)
    nomeautore = yt.author


    listCommenti = extractVideoComments(videoUrl, numCommenti)
    cd.createOrUpdateDataset(listCommenti, nomeautore, titolo, topic, "YouTube")





ytComments()
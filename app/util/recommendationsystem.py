from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine
from konlpy.tag import Okt
import pandas as pd
import numpy as np
import re

engine = create_engine('mysql+pymysql://root:7419553@localhost:3305/dmtime?charset=utf8mb4')

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다', "내", "네", "니다"]


def __Preprocessing(title):
    # regular expression
    regex_data = []
    for t in title:
        regex_data.append(re.sub('[^ㄱ-ㅣ가-힣A-Z]', '', t))

    # processing stopword and token length < 1
    okt = Okt()
    processed_data = []
    for t in regex_data:
        sent = okt.nouns(t)
        sent = [token for token in sent if token not in stopwords]
        sent = [token for token in sent if len(sent) > 1]
        sent = " ".join(sent)
        processed_data.append(sent)

    return processed_data


def Recomendation(post_id):
    # find post_id and title more than a week
    query = 'select post.id, post.title from post where post.posted_datetime > (now() - interval 1 week);'

    # make dataframe
    dataframe = pd.DataFrame(engine.execute(query).fetchall(), columns=['postId', 'title'])

    start_idx = dataframe['postId'][0]

    title = np.array(dataframe['title'].tolist())
    processing_data = __Preprocessing(title)

    # TF-ID
    tfidf = TfidfVectorizer()
    tfidf.fit(processing_data)
    tfidf_dataframe = pd.DataFrame(
        tfidf.transform(processing_data).toarray(),
        columns=sorted(tfidf.vocabulary_),
        index=dataframe['postId']
    )

    # calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf_dataframe, tfidf_dataframe)

    sim_scores = [(i+post_id, c) for i, c in enumerate(cosine_sim[post_id-start_idx]) if c > 0 and i != (post_id-start_idx)]

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    df = pd.DataFrame(sim_scores, columns=['postId', 'cosine similarity'])
    return np.array(df['postId'].tolist())


print(Recomendation(6))
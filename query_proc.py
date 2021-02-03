import numpy as np
from math import log
from nltk.stem import WordNetLemmatizer
from collections import defaultdict                                # only for mapping of pos_tag as noun kept at default
from nltk import pos_tag
lemmatizer = WordNetLemmatizer()                                   # Init Lemmatizer


def reading_dic():                                                  # reading dictionary from disk
    with open('dictionary', "r") as file:
        dictionary = [word.strip() for word in file]
    file.close()
    return dictionary


def read_df():                                                       # df calculated in index file
    df = {}
    with open('df', "r") as file:
        rows = (line.split(':') for line in file)
        for row in rows:
            row[1] = int(row[1])
            df[row[0]] = row[1]
    file.close()
    return df


def q_tf_idf_score(query, df):
    q_tf = {}
    q_tf_idf = {}
    for token in query:
        q_tf[token] = query.count(token)
    for token in q_tf:
        q_tf_idf[token] = np.round(((q_tf[token]) * ((log(df[token], 10))/56)),5)
    print(q_tf)
    print(q_tf_idf)
    return q_tf_idf


def make_query(query):
    tokens = []
    query = query.split()
    stopfile = open("Stopword-List.txt", "r")
    stopwords = stopfile.read().split()
    stopfile.close()
    tag_map = defaultdict(lambda: 'n')                                       # for mapping of pos_tag
    tag_map['J'] = 'a'
    tag_map['V'] = 'v'
    tag_map['R'] = 'r'
    query = [word for word in query if word not in stopwords]
    for token, tag in pos_tag(query):
        tokens.append(lemmatizer.lemmatize(token, tag_map[tag[0]]))         # lemmatization with POS_tag
    print(tokens)
    return tokens


def q_vectorization(q_tf_idf, vocab):
    q = np.zeros((len(vocab)))
    for token in q_tf_idf:
        q[vocab.index(token)] = q_tf_idf[token]
    return q


def cosine_similarity(d_vec, q_vec):
    similar = {}
    docs, terms = d_vec.shape
    doc = 0
    while doc != docs:
        similar[doc] = np.dot(d_vec[doc], q_vec) / (np.sqrt(np.sum(d_vec[doc]**2)) * np.sqrt(np.sum(q_vec**2)))
        doc += 1
    return similar


def ranking(sim):
    ans = {}
    for doc in sim:
        if sim[doc] > 0.0005:
            ans[doc] = sim[doc]
    res = sorted(ans.items(), key=lambda x: x[1], reverse=True)
    res = [doc[0] for doc in res]
    return res


def start(query):
    vocab = reading_dic()
    print(vocab)
    df = read_df()
    d_vec = np.loadtxt('d_vec.csv', delimiter=',')
    query = make_query(query)
    for word in query:
        if word not in vocab:
            res = ['NO MATCH, make query again']
            return res
    q_tf_idf = q_tf_idf_score(query, df)
    q_vec = q_vectorization(q_tf_idf, vocab)
    sim = cosine_similarity(d_vec, q_vec)
    res = ranking(sim)
    print(res)
    print('length', len(res))
    return res



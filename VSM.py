import math
import numpy as np


def reading_dic():
    with open('dictionary', "r") as file:
        dictionary = [word.strip() for word in file]
    file.close()
    return dictionary


def reading_tf():                                      # tf calculated in index file and stored on disk
    tf = {}
    with open('tf', "r") as file:
        rows = (line.split(':') for line in file)
        for row in rows:
            res = row[0].strip(')(').split(', ')
            res[0] = res[0].strip("''")
            res[1] = int(res[1])
            row[1] = int(row[1])
            tf[res[0], res[1]] = row[1]

    file.close()
    return tf


def read_df():                                      # df calculated in index file
    df = {}
    with open('df', "r") as file:
        rows = (line.split(':') for line in file)
        for row in rows:
            row[1] = int(row[1])
            df[row[0]] = row[1]
    file.close()
    return df


def tf_idf_score(tf, df):
    tf_idf = {}
    for (term, doc) in tf:
        if term == 'â\\xa0':                            # junk term
            continue
        else:
            tf_idf[term, doc] = ((tf[term, doc]) * ((math.log(df[term], 10))/56))           # idf = tf * idf
    return tf_idf


def doc_vectorization(vocab, tf_idf):
    d = np.zeros((56, len(vocab)))
    for (term, doc) in tf_idf:
        d[doc][vocab.index(term)] = tf_idf[term, doc]
    return d


def start():
    vocab = reading_dic()
    print(vocab)
    df = read_df()
    tf = reading_tf()
    tf_idf = tf_idf_score(tf, df)
    d_vec = doc_vectorization(vocab, tf_idf)
    print('shape of document vectors', d_vec.shape)
    np.savetxt('d_vec.csv', d_vec, delimiter=',', fmt='%1.3f')


def main():
    start()


if __name__ == '__main__':
    main()
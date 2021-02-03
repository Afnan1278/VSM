import os
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from collections import defaultdict                                # only for mapping of pos_tag as noun kept at default
lemmatizer = WordNetLemmatizer()                                   # # Init lemmatizer


def preprocessing(f, stopwords, punctuations, tag_map):
    no_punc = ' '
    filtered_words = []
    f.readline()                                                         # excluding first line of doc
    for line in f:
        line = line.lower()                                                  # CASE FOLDING
        for char in line:
            if char not in punctuations:
                no_punc += char
            else:
                no_punc += " "                                                 # replacing punctuation with space
        words = no_punc.split()
    tokens = [word for word in words if word not in stopwords]                 # removing stopwords
    for token, tag in pos_tag(tokens):
        filtered_words.append(lemmatizer.lemmatize(token, tag_map[tag[0]]))      # lemmatization with POS_tag

    filtered_words = [word for word in filtered_words if len(word) > 1]         # removing 1 or 0 length words

    return filtered_words


def create_index(index_list, filtered_words, id):
    for term in filtered_words:
        if term not in index_list:
            index_list[term] = [id]
        else:
            if id not in index_list[term]:
                index_list[term].append(id)
    return index_list


def cal_tf(tf, tokens, id):
    for token in tokens:
        tf[token, id] = tokens.count(token)
    return tf


def cal_df(dictionary):
    df = {}
    for term in dictionary:
        df[term] = len(dictionary[term])
    return df


def tag_match():                                                                # for mapping of pos_tag
    tag_map = defaultdict(lambda: 'n')
    tag_map['J'] = 'a'
    tag_map['V'] = 'v'
    tag_map['R'] = 'r'
    return tag_map

def reading_corpus():
    stopfile = open("Stopword-List.txt", "r")
    stopwords = stopfile.read().split()
    stopfile.close()
    dirr = os.getcwd()                                                          # getting current path
    file = os.path.join(dirr, "Trump Speechs")
    punctuations = '''!()-[]{};:'",<>./?—@#$%^&*_~'''
    docid = 0
    tag_map = tag_match()
    index_list = {}
    term_freq = {}
    while docid < 56:
        file1 = os.path.join(file, "speech_"+str(docid)+".txt")
        f = open(file1, "r")
        filtered_words = preprocessing(f, stopwords, punctuations, tag_map)
        index_list = create_index(index_list, filtered_words, docid)
        term_freq = cal_tf(term_freq,filtered_words,docid)
        docid += 1
    df = cal_df(index_list)
    print('no. dictionary words ', len(index_list))
    # print(term_freq)
    return index_list, term_freq, df


def df_save(df):                                       # save document freq on disk
    f = open('df', 'w')
    for key, value in df.items():
        f.write('%s:%s\n' % (key, value))
    f.close()


def tf_save(tf):                                       # save term freq on disk
    with open('tf', 'w') as f:
        for key, value in tf.items():
            f.write('%s:%s\n' % (key, value))
    f.close()
    print(tf)


def dic_save(dictionary):                                   # save dictionary on disk
    with open('dictionary', 'w') as f:
        for term in dictionary:
            f.write('%s\n' % term)
    f.close()
    print(dictionary)


def main():
    dictionary, tf, df = reading_corpus()
    dic_save(dictionary)
    tf_save(tf)
    df_save(df)


if __name__ == '__main__':
    main()
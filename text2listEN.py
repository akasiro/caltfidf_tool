# coding:utf-8
import nltk
import re
import string
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from nltk.probability import FreqDist

# 标点符号过滤
def filter_punctuation(words):
    illegal_char = string.punctuation + '【·！…（）—：“”？《》、；】'
    punc = list(illegal_char)
    new_words = [word for word in words if word not in punc]
    return new_words

# 处理停止词
def filter_stop_words(words):
    stops=set(stopwords.words('english'))
    words = [word for word in words if word.lower() not in stops]
    return words

# 分词、提取词干
def Word_segmentation_and_extraction(text):
    words=nltk.word_tokenize(text)
    stemmerlan=LancasterStemmer()
    for i in range(len(words)):
        words[i] = stemmerlan.stem(words[i])
    return words

# 低频词过滤
# def filter_low_frequency_words(words):
#     fdist = FreqDist(words)
#     return fdist

def text2listfull(text):
    words = Word_segmentation_and_extraction(text)
    words_nostop = filter_stop_words(words)
    words_no_punc = filter_punctuation(words_nostop)
    return words_no_punc

if __name__ == '__main__':
    with open('test.txt', 'r') as f:
        test = f.read()
    w = text2listfull(test)
    print(w)
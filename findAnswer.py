'''
Author: guanliyang 18622300031@163.com
Date: 2023-06-14 09:02:10
LastEditors: guanliyang 18622300031@163.com
LastEditTime: 2023-06-14 15:23:47
FilePath: \FAQ\findAnswer.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import jieba
import jieba.analyse
from collections import Counter
 
def word_2_vec(words1, words2):
    # 词向量
    words1_info = jieba.analyse.extract_tags(words1, withWeight=True)
    words2_info = jieba.analyse.extract_tags(words2, withWeight=True)
    # 转成counter不需要考虑0的情况
    words1_dict = Counter({i[0]: i[1] for i in words1_info})
    words2_dict = Counter({i[0]: i[1] for i in words2_info})
    bags = set(words1_dict.keys()).union(set(words2_dict.keys()))
    # 转成list对debug比较方便吗，防止循环集合每次结果不一致
    bags = sorted(list(bags))
    vec_words1 = [words1_dict[i] for i in bags]
    vec_words2 = [words2_dict[i] for i in bags]
    # 转numpy
    vec_words1 = np.asarray(vec_words1, dtype=float)
    vec_words2 = np.asarray(vec_words2, dtype=float)
    return vec_words1, vec_words2

def cosine_similarity(v1, v2):
    # 余弦相似度
    v1, v2 = np.asarray(v1, dtype=float), np.asarray(v2, dtype=float)
    up = np.dot(v1, v2)
    down = np.linalg.norm(v1) * np.linalg.norm(v2)
    return round(up / down, 3)

def calculate_cosine_similarity(text1, text2):
    vectorizer = CountVectorizer()
    corpus = [text1, text2]
    vectors = vectorizer.fit_transform(corpus)
    similarity = cosine_similarity(vectors)
    return similarity[0][1]


def get_answer(sentence1):
    score = []
    inputQ = open('Answer.txt', 'r', encoding='utf-8')
    line_index = 0
    for line in inputQ:
        if line_index %2 ==0: #说明是问题
            score.append(cosine_similarity(*word_2_vec(line, sentence1)))
        line_index += 1
    if len(set(score)) == 1:
        print('暂时无法找到您想要的答案。')
        return '暂时无法找到您想要的答案。'
    else:
        index = score.index(max(score))
        file = open('Answer.txt', 'r',encoding='utf-8').readlines()
        print("答案是："+file[index])
        return file[index*2+1]
   



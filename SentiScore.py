#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/9 下午3:04
# @Author  : Shihan Ran
# @Site    : 
# @File    : thoughts.py
# @Software: PyCharm

# this file is aimed to process sentence to word
# and use sentiment dict to score a sentence

import numpy
import jieba

stop_words = [w.strip() for w in open('./dict/notWord.txt', 'r', encoding='GBK').readlines()]
stop_words.extend(['\n','\t',' '])

def Sent2Word(sentence):
   # 去除停用词
   global stop_words

   words = jieba.cut(sentence)
   words = [w for w in words if w not in stop_words]

   return words

# 加载各种词典
def LoadDict():
   # 情感词
   pos_words = open('./dict/pos_word.txt').readlines()
   pos_dict = {}
   for w in pos_words:
      word, score= w.strip().split(',')
      pos_dict[word] = float(score)

   neg_words = open('./dict/neg_word.txt').readlines()
   neg_dict = {}
   for w in neg_words:
      word, score = w.strip().split(',')
      neg_dict[word] = float(score)

   # 否定词 ['不', '没', '无', '非', '莫', '弗', '勿', '毋', '未', '否', '别', '無', '休', '难道']
   not_words = open('./dict/notDict.txt').readlines()
   not_dict = {}
   for w in not_words:
      word = w.strip()
      not_dict[word] = float(-1)

   #程度副词 {'百分之百': 10.0, '倍加': 10.0, ...}
   degree_words = open('./dict/degreeDict.txt').readlines()
   degree_dict = {}
   for w in degree_words:
       word,score = w.strip().split(',')
       degree_dict[word] = float(score)

   return pos_dict, neg_dict, not_dict, degree_dict

# 定位句子中的 情感词 否定词 程度副词的 【位置】
def LocateSpecialWord(pos_dict, neg_dict, not_dict, degree_dict, sent):
   pos_word = {}
   neg_word = {}
   not_word = {}
   degree_word = {}

   for index, word in enumerate(sent):
      if word in pos_dict:
         pos_word[index] = pos_dict[word]
         # print('pos', word)
      elif word in neg_dict:
         neg_word[index] = neg_dict[word]
         # print('neg', word)
      elif word in not_dict:
         not_word[index] = -1
         # print('not', word)
      elif word in degree_dict:
         degree_word[index] = degree_dict[word]
         # print('degree', word)

   return pos_word, neg_word, not_word, degree_word

# 计算该句子的分数
def ScoreSent(pos_word, neg_word, not_word, degree_word, words):
   W=1
   score=0

   # 存所有情感词的位置的列表
   pos_locs = list(pos_word.keys())
   neg_locs = list(neg_word.keys())
   not_locs = list(not_word.keys())
   degree_locs = list(degree_word.keys())

   posloc=-1  # 已检测到多少词
   negloc=-1

   # 遍历句中所有单词words，i为单词绝对位置
   for i in range(0,len(words)):
       # 如果该词为积极词
       if i in pos_locs:
           # loc为情感词位置列表的序号
           posloc += 1
           # 直接添加该情感词分数
           score += W * float(pos_word[i])

           # if posloc < len(pos_locs)-1:
           #     # 判断该情感词与下一情感词之间是否有否定词或程度副词
           #     # j为绝对位置
           #     # print(pos_locs)
           #     for j in range(pos_locs[posloc], pos_locs[posloc+1]):
           #         # 如果有否定词
           #         if j in not_locs:
           #            W *= -1
           #         # 如果有程度副词
           #         elif j in degree_locs:
           #            # print('degree', words[j])
           #            W *= degree_word[j]
           #         # else:
           #         #     W *= 1

       elif i in neg_locs:
          # loc为情感词位置列表的序号
          negloc += 1
          # 直接添加该情感词分数
          # print(i)
          # print(score, W * float(neg_word[i]))
          score += (-1) * W * float(neg_word[i])

          # if negloc < len(neg_locs) - 1:
          #    # 判断该情感词与下一情感词之间是否有否定词或程度副词
          #    # j为绝对位置
          #    for j in range(neg_locs[negloc], neg_locs[negloc + 1]):
          #       # 如果有否定词
          #       if j in not_locs:
          #          # print('not', words[j])
          #          W *= -1
          #       # 如果有程度副词
          #       elif j in degree_locs:
          #          # print('degree', words[j])
          #          W *= degree_word[j]
          #       # else:
          #       #     W = 1

   # print(numpy.sign(score)*numpy.log(abs(score)))
   return numpy.sign(score)

# # to find the score of sentiment
# def SentiFeatures(text, k):
#     pos, neg = [0, 0]
#     n = len(text) / 2  # 有n篇news:[[title],[content]]
#     global pos_dict, neg_dict, not_dict, degree_dict
#
#     title_score = []
#     for title in [2 * i for i in range(0, int(n))]:  # [0,2,4,6,...]
#         pos_word, neg_word, not_word, degree_word = SentiScore. \
#             LocateSpecialWord(pos_dict, neg_dict, not_dict, degree_dict,
#                               sorted(set(text[title]), key=text[title].index))
#         title_score.append(SentiScore.ScoreSent(pos_word, neg_word, not_word, degree_word,
#                                                 sorted(set(text[title]), key=text[title].index)))
#         pos = len(pos_word) * k
#         neg = len(neg_word) * k
#     TitleScore = round(np.mean(title_score)) * k
#
#     content_score = []
#     for content in [2 * i + 1 for i in range(0, int(n))]:  # [1,3,5,7,...]
#         pos_word, neg_word, not_word, degree_word = SentiScore. \
#             LocateSpecialWord(pos_dict, neg_dict, not_dict, degree_dict,
#                               sorted(set(text[content]), key=text[content].index))
#         content_score.append(SentiScore.ScoreSent(pos_word, neg_word, not_word, degree_word,
#                                                   sorted(set(text[content]), key=text[content].index)))
#         pos += len(pos_word)
#         neg += len(neg_word) + len(not_dict)
#     ContentScore = round(np.mean(content_score))
#
#     PosWord = round(pos / (10 * n))
#     NegWord = round(neg / (10 * n))
#
#     return n, TitleScore, ContentScore, PosWord, NegWord
#
# # feature extraction
# def TextFeatures(text, k):
#
#     features = {}
#     # features['length'] = sum([len(w) for w in text])
#
#     features['news_num'], features['title_score'], features['content_score'], \
#     features['pos_word'], features['neg_word'] = SentiFeatures(text,k)
#
#     return features
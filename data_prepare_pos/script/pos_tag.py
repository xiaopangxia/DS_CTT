# -*- coding:utf-8 -*-
import sys
import requests
import json
import re
import codecs
import jieba.posseg as pseg
reload(sys)
sys.setdefaultencoding('gbk')


def t_2_bi():
    # 整理T标注为BI标注
    out_file = open("../data_file/sentence_tag_standard_5.txt", 'a')
    pre_flag = 0
    with open("../data_file/sentence_vertical_tag_5.txt", 'r') as in_file:
        for line in in_file.readlines():
            if pre_flag == 0 and "	T" in line:
                out_file.write(line.replace("	T", "	B"))
                pre_flag = 1
            elif pre_flag == 1 and "	T" in line:
                out_file.write(line.replace("	T", "	I"))
                pre_flag = 1
            elif not "	T" in line:
                out_file.write(line.replace("########", ''))
                pre_flag = 0

def jieba_pos():
    # jieba分词与词性引入
    out_file = codecs.open("../data_file/sentence_tag_5_pos.txt", 'a', encoding='utf8')
    with codecs.open('../data_file/sentence_tag_standard_5.txt', 'r', encoding='utf8') as in_file:
        word_list = []
        tag_list = []
        for line in in_file.readlines():
            if len(line.split())>1:
                word_list.append(line.split()[0])
                tag_list.append(line.split()[1])
            else:
                # 凑够了一句话
                sentence = ''.join(word_list)
                seg = pseg.cut(sentence)
                flag_list = []
                for w in seg:
                    for char in w.word:
                        flag_list.append(w.flag)
                for i in range(len(word_list)):
                    if flag_list[i] == 't' and 'O' in tag_list[i]:
                        tag_list[i] = 'T'
                    out_file.write(word_list[i]+'\t'+tag_list[i]+'\r\n')
                out_file.write('\r\n')
                if len(word_list) != len(flag_list):
                    print sentence
                word_list = []
                tag_list = []


def pos_t_2_bi():
    # 整理jieba分词后的T标注为BI标注
    out_file = open("../data_file/sentence_tag_5_final.txt", 'a')
    pre_flag = 'O'
    with open("../data_file/sentence_tag_5_pos.txt", 'r') as in_file:
        for line in in_file.readlines():
            if pre_flag == 'O' and "	T" in line:
                out_file.write(line.replace("	T", "	B"))
                pre_flag = 'T'
            elif (pre_flag == 'T' or pre_flag == 'I') and "	T" in line:
                out_file.write(line.replace("	T", "	I"))
                pre_flag = 'T'
            elif "	I" in line or '	B' in line:
                out_file.write(line)
                pre_flag = 'I'
            elif not "	T" in line:
                out_file.write(line)
                pre_flag = 'O'

def only_jieba():
    # only jieba词性标注标注
    out_file = open("../data_file/sentence_tag_5_only_jieba.txt", 'a')
    pre_flag = 'O'
    with open("../data_file/sentence_tag_5_pos.txt", 'r') as in_file:
        for line in in_file.readlines():
            if pre_flag == 'O' and "	T" in line:
                out_file.write(line.replace("	T", "	B"))
                pre_flag = 'T'
            elif (pre_flag == 'T' or pre_flag == 'I') and "	T" in line:
                out_file.write(line.replace("	T", "	I"))
                pre_flag = 'T'
            elif not "	T" in line:
                out_file.write(line.replace('	B', '	O').replace('	I', '	O'))
                pre_flag = 'O'













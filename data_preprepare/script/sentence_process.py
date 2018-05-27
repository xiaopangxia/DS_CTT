# -*- coding:utf-8 -*-
import sys
import re
import os
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


class SentenceProcess():
    """
    先从大量百科页面中整理出句子,
    再按照top时间属性值匹配出一批训练集
    """

    @classmethod
    def html2sent_list(cls, html_file):
        try:
            my_soup = BeautifulSoup(html_file, "lxml")
            html_content = str(my_soup.find(name='div', attrs={"class": "main-content"}))
            # 首先去除可能导致误差的script和css，之后再去标签
            tempResult = re.sub('<script([\s\S]*?)</script>', '', html_content)
            tempResult = re.sub('<style([\s\S]*?)</style>', '', tempResult)
            tempResult = re.sub('(?is)<.*?>', '', tempResult)
            tempResult = tempResult.replace(' ', '')
            tempResultArray = tempResult.split('\n')
            # print tempResult

            data = []
            string_data = []
            result_data = ''
            summ = 0
            count = 0

            # 计算长度非零行的行数与总长度
            for oneLine in tempResultArray:
                if (len(oneLine) > 0):
                    data.append(len(oneLine))
                    string_data.append(oneLine)
                    summ += len(oneLine)
                    count += 1
            # print 'averange is:'+ str(summ/count)
            for oneLine in string_data:
                # if len(oneLine) >= summ/count+180:
                if len(oneLine) >= 120:
                    # print oneLine
                    result_data += oneLine

            return re.split(u"[。;；\s]", unicode(result_data))
        except Exception, e:
            print e
            return []

    @classmethod
    def save_all_sentence(cls):
        """
        将百科页面中的句子逐条保存下来
        :return:
        """
        file_list = os.listdir("../baidu_raw_page/")
        for file in file_list:
            with open("../baidu_raw_page/" + file, 'r') as in_file:
                html_file = in_file.read()
            sent_list = SentenceProcess.html2sent_list(html_file)
            with open("../data_file/sentence_set.txt", 'a') as out_file:
                for line in sent_list:
                    if len(line) > 15:
                        out_file.write(line + "\n")
            print file


    @classmethod
    def temporal_sentence_candidate(cls):
        """
        筛选出带有时间表达式的句子,
        并标注时间表达式位置,暂未标出
        :return:
        """
        temporal_expression_list = []
        with open("../data_file/temporal_expression_deduplicate_len_sort.txt", 'r') as in_file:
            for line in in_file:
                temporal_expression_list.append(line.split()[0])


        out_file = open("../data_file/temporal_sentence_candidate_pure.txt", 'a')
        with open("../data_file/sentence_set.txt", 'r') as in_file:
            for line in in_file.readlines():
                for tmp_exp in temporal_expression_list[0:210000]:
                    if tmp_exp in line and len(unicode(tmp_exp))>=2:
                        out_file.write(line)
                        break


    @classmethod
    def sentence_deduplicate(cls, in_file_name, out_file_name):
        """
        候选句子去重
        :return:
        """
        sentence_dict = {}
        with open(in_file_name, 'r') as in_file:
            for line in in_file.readlines():
                sentence_dict[line] = 1
        with open(out_file_name, 'a') as out_file:
            for sentence in sentence_dict:
                out_file.write(sentence)





# SentenceProcess.save_all_sentence()
# SentenceProcess.temporal_sentence_candidate()
# SentenceProcess.sentence_deduplicate("../data_file/temporal_sentence_candidate_pure.txt", "../data_file/temp_sent_cand_super_pure_deduplicate.txt")


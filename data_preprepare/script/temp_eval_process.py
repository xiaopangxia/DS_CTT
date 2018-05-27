# -*- coding:utf-8 -*-
import sys
import re
import json
import os

reload(sys)
sys.setdefaultencoding('utf-8')


class TempEvalProcess():
    """
    先将temp_eval的训练集和测试集由tab文件
    组织成每句两行,逐字标记的格式
    例:
    五   月   一   日   我   在   天   塔   湖   划   船   .
    T    T   T    T    O    O   O    O    O    O   O    O
    """
    @classmethod
    def tab2txt(cls, seg_file, timex_file, out_file):
        """
        从一个基本分词文件和一个时间表达式文件
        到一个逐字标注的txt文件
        :param seg_file:基本分词文件
        :param timex_file:时间标注文件
        :param out_file:输出文件
        :return:
        """
        timex_dict = {}
        with open(timex_file, 'r') as in_file:
            for line in in_file:
                file_id = line.split()[0]
                sent_id = line.split()[1]
                token_id = line.split()[2]
                timex_id = line.split()[4]
                if not timex_dict.get(file_id):
                    timex_dict[file_id] = {}
                if not timex_dict[file_id].get(sent_id):
                    timex_dict[file_id][sent_id] = {}
                if not timex_dict[file_id][sent_id].get(token_id):
                    timex_dict[file_id][sent_id][token_id] = timex_id


        seg_dict = {}
        with open(seg_file, 'r') as in_file:
            for line in in_file.readlines():
                file_id = line.split()[0]
                sent_id = line.split()[1]
                token_id = line.split()[2]
                token_word = line.split()[-1]
                if not seg_dict.get(file_id):
                    seg_dict[file_id] = {}
                if not seg_dict[file_id].get(sent_id):
                    seg_dict[file_id][sent_id] = {"sent": [], "tag": []}

                is_timex = 0
                if timex_dict.get(file_id):
                    if timex_dict[file_id].get(sent_id):
                        if timex_dict[file_id][sent_id].get(token_id):
                            is_timex = 1
                if is_timex == 1:
                    for char in unicode(token_word):
                        seg_dict[file_id][sent_id]["sent"].append(char)
                        seg_dict[file_id][sent_id]["tag"].append("T")
                else:
                    for char in unicode(token_word):
                        seg_dict[file_id][sent_id]["sent"].append(char)
                        seg_dict[file_id][sent_id]["tag"].append("O")

        # 只句子
        with open(out_file, 'a') as out_file:
            for file_id in seg_dict:
                for sent_id in seg_dict[file_id]:
                    for i in range(len(seg_dict[file_id][sent_id]["sent"])):
                        the_char = seg_dict[file_id][sent_id]["sent"][i]
                        out_file.write(the_char)
                    out_file.write("\n")

        # 纵向
        with open(out_file, 'a') as out_file:
            for file_id in seg_dict:
                for sent_id in seg_dict[file_id]:
                    for i in range(len(seg_dict[file_id][sent_id]["sent"])):
                        the_char = seg_dict[file_id][sent_id]["sent"][i]
                        the_tag = seg_dict[file_id][sent_id]["tag"][i]
                        out_file.write(the_char+"\t"+the_tag+"\n")
                    out_file.write("\n")

        # 横向
        with open(out_file, 'a') as out_file:
            for file_id in seg_dict:
                for sent_id in seg_dict[file_id]:
                    for i in range(len(seg_dict[file_id][sent_id]["sent"])):
                        # print seg_dict[file_id][sent_id]["sent"][i], seg_dict[file_id][sent_id]["tag"][i]
                        the_char = seg_dict[file_id][sent_id]["sent"][i]
                        out_file.write(the_char+"\t")
                    out_file.write("\n")
                    for i in range(len(seg_dict[file_id][sent_id]["sent"])):
                        the_tag = seg_dict[file_id][sent_id]["tag"][i]
                        out_file.write(the_tag+"\t")
                    out_file.write("\n")





# TempEvalProcess.tab2txt("../temp_eval_2/train/base-segmentation.tab", "../temp_eval_2/train/timex-extents.tab", "../temp_eval_2/train/train_temporal_tag.txt")
# TempEvalProcess.tab2txt("../temp_eval_2/test/base-segmentation.tab", "../temp_eval_2/test/timex-extents.tab", "../temp_eval_2/test/test_temporal_tag.txt")


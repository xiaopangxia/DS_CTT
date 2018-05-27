# -*- coding:utf-8 -*-
import sys
import re
import json

reload(sys)
sys.setdefaultencoding('utf-8')


class TextMatchTag():
    """
    将数字做泛化,如1827年4月七日,泛华为####年#月#日
    """

    @classmethod
    def digit_trans(cls, temp_str):
        digit_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                      '一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '〇', ]
        for digit in digit_list:
            temp_str = temp_str.replace(digit, '#')
        return temp_str

    @classmethod
    def digit_special_tag(cls):
        digit_temp_dict = {}
        temp_list = []
        with open("../data_file/temporal_expression_5.txt", 'r') as in_file:
            for line in in_file:
                temp_list.append(line.split()[0])
                digit_temp_dict[cls.digit_trans(line.split()[0])] = 1


        special_digit_list = []
        for key in digit_temp_dict:
            if '#' in key:
                special_digit_list.append(key)

        sentence_file = "../data_file/temporal_sentence_candidate.txt"
        out_file = open("../data_file/sentence_vertical_tag_5.txt", 'a')
        tag_cnt = 0
        untag_cnt = 0
        with open(sentence_file, 'r') as in_file:
            for line in in_file.readlines():
                sent_line = unicode(line.strip())
                tag_line = unicode(line.strip())
                special_sent_line = unicode(cls.digit_trans(line.strip()))
                special_tag_line = unicode(cls.digit_trans(line.strip()))
                for tmp_exp in temp_list:
                    if tmp_exp in line:
                        tmp_tag_line = unicode(line.strip()).replace(unicode(tmp_exp), 'T' * len(unicode(tmp_exp)))
                        new_tag_line = ''
                        for i in range(len(tag_line)):
                            if tmp_tag_line[i] == 'T':
                                new_tag_line += 'T'
                            else:
                                new_tag_line += tag_line[i]
                        tag_line = new_tag_line


                for tmp_exp in special_digit_list:
                    if tmp_exp in special_sent_line:
                        tmp_tag_line = special_sent_line.replace(unicode(tmp_exp), 'T' * len(unicode(tmp_exp)))
                        new_tag_line = ''
                        for i in range(len(special_tag_line)):
                            if tmp_tag_line[i] == 'T':
                                new_tag_line += 'T'
                            else:
                                new_tag_line += special_tag_line[i]
                        special_tag_line = new_tag_line

                if 'T' in tag_line or 'T' in special_tag_line:
                    for i in range(len(sent_line)):
                        if sent_line[i] == tag_line[i] and special_tag_line[i] != 'T':
                            tag = "O"
                        else:
                            tag = "T"
                        out_file.write(sent_line[i] + "\t" + tag + "\r\n")
                    out_file.write("。\tO\r\n")
                    out_file.write("########\r\n")
                    tag_cnt += 1
                else:
                    with open("../data_file/untag_sentence_5.txt", 'a') as untag_file:
                        untag_file.write(line)
                    untag_cnt += 1
                    if untag_cnt % 100 == 0:
                        print "tag:%s\tuntag:%s" % (str(tag_cnt), str(untag_cnt))



TextMatchTag.digit_special_tag()


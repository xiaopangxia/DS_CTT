# -*- coding:utf-8 -*-
import sys
import re
import json
reload(sys)
sys.setdefaultencoding('utf-8')

class TemporalFilter():
    @classmethod
    def long_temporal_filter(cls):
        """
        过滤出长时间表达式
        过滤标准:
            表达式长度大于5个字符的非英文文本
        西文字符占比不超过1/3

        :return:
        """

        out_file = open("../data_file/temporal_expression_5.txt", 'a')
        with open("../data_file/temporal_expression_deduplicate_clean.txt", 'r') as in_file:
            for line in in_file.readlines():
                temporal_exp = unicode(line.split()[0].strip())
                if len(temporal_exp) >= 5 and "《" not in temporal_exp:
                    digit_cnt = 0
                    for char in temporal_exp:
                        if char.isupper() or char.islower():
                            digit_cnt += 1
                    if digit_cnt*3 <= len(temporal_exp):
                        out_file.write(line.strip()+"\n")



# TemporalFilter.long_temporal_filter()



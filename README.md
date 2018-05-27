# DS_CTT
## Distant supervision for Chinese Temporal Tagging<br>
利用CN-DBPedia的triples做远程监督，进行中文时间表达式标注。<br>
序列标注模型采用BiLSTM+CRF。<br>

## DS_CTT介绍<br>
百科语料经来自CN-DBPedia的时间相关三元组远程监督标注，作为序列标注模型BiLSTM+CRF的训练集。<br>
### raw_pages来源： <br>
      百度百科随机页面3万条
### Bike_triples.txt文件：<br>
      来自知识工场2015年dump文件，http://openkg.cn/dataset/cndbpedia <br>
      
### 代码使用：
数据准备部分用python2.7写的，序列标注模型python3.5+Tensorflow

### 总体框架图<br>
![框架图](https://github.com/xiaopangxia/DS_CTT/blob/master/images/flow_1.PNG)<br>
### 训练集标注示意图（两轮标注）：<br>
##### 第一轮较长时间属性值文本匹配<br>
![训练集标注示意图](https://github.com/xiaopangxia/DS_CTT/blob/master/images/flow_2.PNG)<br>
##### 第二轮加入jieba词性标注的结果<br>
![pos tagging](https://github.com/xiaopangxia/DS_CTT/blob/master/images/flow_4.PNG)<br>
### 序列标注模型框架图：<br>
![序列标注模型BiLSTM+CRF](https://github.com/xiaopangxia/DS_CTT/blob/master/images/flow_3.PNG)


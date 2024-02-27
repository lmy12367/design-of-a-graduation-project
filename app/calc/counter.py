import jieba

txt = open("1.txt", "r", encoding='utf-8').read()# 2.全职法师   加载txt文本
words = jieba.cut(txt)# 返回可迭代的数据
stop = open("stopwords.txt", "r", encoding='utf-8').read()# 加载停用词表

counts = {}# 创建列表

for word in words:
    if word not in stop:# 去除停用词
        if len(word) == 1:
            continue# 如果字长为1则去除
        else:
            counts[word] = counts.get(word, 0) + 1# 字长不为1且不是停用词的词，频率加1
items = list(counts.items())# 转换为列表

items.sort(key=lambda x: x[1], reverse=True)# 对词频进行降序排序
for i in range(4):#输出频率最高的前十五个词
    word, count = items[i]
    print("{0:<10}{1:<5}".format(word, count))# 输出

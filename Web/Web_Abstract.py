# import sys
# from imp import reload
from textrank4zh import TextRank4Keyword, TextRank4Sentence

# try:
#     # reload方法用于对已经加载的模块进行重新加载，一般用于原模块有变化的情况
#     reload(sys)
#     # 设置系统的默认编码方式，仅本次有效，因为setdefaultencoding函数在被系统调用后即被删除
#     sys.setdefaultencoding('utf-8')
# except:
#     pass


def getSummary(str):
    string_abstract = []
    text = str
    # 创建分词类的实例
    tr4w = TextRank4Keyword()
    # 对文本进行分析，设定窗口大小为2，并将英文单词小写
    tr4w.analyze(text=text, lower=True, window=2)
    # 创建分句类的实例
    tr4s = TextRank4Sentence()
    # 英文单词小写，进行词性过滤并剔除停用词
    tr4s.analyze(text=text, lower=True, source='all_filters')
    for item in tr4s.get_key_sentences(num=3):
        string_abstract += item.sentence
    return string_abstract


with open('put-article.txt', 'r', encoding='utf-8') as article:
    text = article.read().replace('\n', '')
    summarize_text = getSummary(text)
    with open('out-summary.txt', 'w', encoding='utf-8') as abstract:
        for n in summarize_text:
            abstract.write(n)
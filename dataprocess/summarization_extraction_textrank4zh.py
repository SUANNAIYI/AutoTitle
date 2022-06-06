# 导入系统模块
import sys
# imp模块提供了一个可以实现import语句的接口
from imp import reload

# 异常处理
try:
    # reload方法用于对已经加载的模块进行重新加载，一般用于原模块有变化的情况
    reload(sys)
    # 设置系统的默认编码方式，仅本次有效，因为setdefaultencoding函数在被系统调用后即被删除
    sys.setdefaultencoding('utf-8')
except:
    pass

# 导入编码转换模块
import codecs
# 从textrank4zh模块中导入提取关键词和生成摘要的类
from textrank4zh import TextRank4Keyword, TextRank4Sentence


def getSummary(str):
    # 待读取的文本文件，一则新闻
    # file = '../examples/corpus/summarization_extraction/taiwanpai.txt'
    # 打开并读取文本文件
    string_abstract = []  # 返回的字符串
    text = str  # 传输入的字符串

    # 创建分词类的实例
    tr4w = TextRank4Keyword()
    # 对文本进行分析，设定窗口大小为2，并将英文单词小写
    tr4w.analyze(text=text, lower=True, window=2)

    # 创建分句类的实例
    tr4s = TextRank4Sentence()
    # 英文单词小写，进行词性过滤并剔除停用词
    tr4s.analyze(text=text, lower=True, source='all_filters')

    for item in tr4s.get_key_sentences(num=3):
        # 打印句子的索引、权重和内容
        # print(item.index, item.weight, item.sentence)
        string_abstract += item.sentence

    return string_abstract

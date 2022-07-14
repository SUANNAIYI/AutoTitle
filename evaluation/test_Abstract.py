from textrank4zh import TextRank4Keyword, TextRank4Sentence


def Abstract(article):
    string_abstract = []
    # text = article.read().replace('\n', '')
    # 创建分词类的实例
    tr4w = TextRank4Keyword()
    # 对文本进行分析，设定窗口大小为2，并将英文单词小写
    tr4w.analyze(text=article, lower=True, window=2)
    # 创建分句类的实例
    tr4s = TextRank4Sentence()
    # 英文单词小写，进行词性过滤并剔除停用词
    tr4s.analyze(text=article, lower=True, source='all_filters')
    for item in tr4s.get_key_sentences(num=3):
        string_abstract += item.sentence
    summarize_text = string_abstract
    with open('out-summary.txt', 'w', encoding='utf-8') as abstract:
        for n in summarize_text:
            abstract.write(n)

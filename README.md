# AutoTitle
此项目为2022软件杯A9赛题：智能创作平台，用于自动生成文章标题
采用bert模型
因为模型问题无法使用大文本进行训练，所以使用先生成摘要再通过摘要训练模型的策略。
生成摘要的代码为dataprocess/dataset.py
train.py文件为训练模型代码
test.py文件为测试代码
感谢920232796提供的训练代码，原文地址https://github.com/920232796/bert_seq2seq

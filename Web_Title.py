# -*- coding: utf-8 -*-
import torch
from bert_seq2seq import Tokenizer, load_chinese_base_vocab
from bert_seq2seq import load_bert

auto_title_model = "train/state_dict/bert_textrank_auto_title_model.bin"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def Title():
    vocab_path = "train/state_dict/roberta_wwm_vocab.txt"  # roberta模型字典的位置
    model_name = "roberta"  # 选择模型名字
    # 加载字典
    word2idx = load_chinese_base_vocab(vocab_path)
    # 定义模型
    bert_model = load_bert(word2idx, model_name=model_name)
    bert_model.set_device(device)
    bert_model.eval()
    # 加载训练的模型参数
    bert_model.load_all_params(model_path=auto_title_model, device=device)
    '''test_data = []
    with open("out-summary.txt", 'r', encoding='utf-8') as abstract:
        lines = abstract.readlines()
        for line in lines:
            line = line.strip()
            test_data.append(line)
    #forecast = []
    for text in test_data:
        with torch.no_grad():
         #global temp
         temp=""
         temp = bert_model.generate(text, beam_size=3)
         #forecast.append(temp)
    #print("预测标题：",temp)
         article_input = open("out-title.txt",'w', encoding='utf-8')
         article_input.write(temp)
    #with open('out-title.txt', 'w', encoding='utf-8') as title:
     #s = "".join(temp)
     #global temp
     #title.write(temp)'''
    test_data = []
    with open("out-summary.txt", 'r', encoding='utf-8') as abstract:
        lines = abstract.readlines()
        for line in lines:
            line = line.strip()
            test_data.append(line)
    forecast = []
    for text in test_data:
        with torch.no_grad():
            temp = bert_model.generate(text, beam_size=3)
            forecast.append(temp)
    with open('out-title.txt', 'w', encoding='utf-8') as title:
        s = "".join(forecast)
        title.write(s)
        print("预测标题：", forecast)


if __name__ == '__main__':
    Title()
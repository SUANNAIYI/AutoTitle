# -*- coding: utf-8 -*-
import torch
from bert_seq2seq import Tokenizer, load_chinese_base_vocab
from bert_seq2seq import load_bert
from rouge import Rouge
import jieba

auto_title_model = "../train/state_dict/bert_textrank_auto_title_model.bin"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == "__main__":
    vocab_path = "../train/state_dict/roberta/roberta_wwm_vocab.txt"  # roberta模型字典的位置
    model_name = "roberta"  # 选择模型名字
    # 加载字典
    word2idx = load_chinese_base_vocab(vocab_path)
    # 定义模型
    bert_model = load_bert(word2idx, model_name=model_name)
    bert_model.set_device(device)
    bert_model.eval()
    # 加载训练的模型参数
    bert_model.load_all_params(model_path=auto_title_model, device=device)
    test_data = []
    with open("../dataprocess/test_abstract.src", 'r', encoding='utf-8') as abstract:
        lines = abstract.readlines()
        for line in lines:
            line = line.strip()
            test_data.append(line)
    title = []
    with open("../dataprocess/test_title.tgt", 'r', encoding='utf-8') as name:
        lines = name.readlines()
        for line in lines:
            line = line.strip()
            line = ' '.join(line)
            title.append(line)
    print(title)
    forecast = []
    for text in test_data:
        with torch.no_grad():
            temp = bert_model.generate(text, beam_size=3)
            forecast.append(temp)
    print(forecast)
    rouge = Rouge()
    for i in range(0, len(forecast)):
        rouge_score = rouge.get_scores(forecast[i], title[i])
        print(rouge_score[0]["rouge-1"])
        print(rouge_score[0]["rouge-2"])
        print(rouge_score[0]["rouge-l"])
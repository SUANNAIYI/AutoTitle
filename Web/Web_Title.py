# -*- coding: utf-8 -*-
import torch
from bert_seq2seq import Tokenizer, load_chinese_base_vocab
from bert_seq2seq import load_bert

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
    with open("out-summary.txt", 'r', encoding='utf-8') as abstract:
        lines = abstract.readlines()
        for line in lines:
            summary = line.strip()
        print(summary)
    for text in summary:
        with torch.no_grad():
            name = bert_model.generate(text, beam_size=3)
        print(name)
    with open('out-title.txt', 'w', encoding='utf-8') as title:
        title.write(name)

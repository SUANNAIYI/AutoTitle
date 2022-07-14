# -*- coding: utf-8 -*-
import torch


def Title(bert_model):
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

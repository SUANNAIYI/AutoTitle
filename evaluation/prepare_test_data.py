import json
from test_Abstract import *
from test_Title import *
from bert_seq2seq import Tokenizer, load_chinese_base_vocab
from bert_seq2seq import load_bert

auto_title_model = "../train/state_dict/bert_textrank_auto_title_model.bin"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
vocab_path = "../train/state_dict/roberta_wwm_vocab.txt"  # roberta模型字典的位置
model_name = "roberta"  # 选择模型名字
# 加载字典
word2idx = load_chinese_base_vocab(vocab_path)
# 定义模型
bert_model = load_bert(word2idx, model_name=model_name)
bert_model.set_device(device)
bert_model.eval()
# 加载训练的模型参数
bert_model.load_all_params(model_path=auto_title_model, device=device)


def read_and_write_data(input_file, output_file):
    fw = open(output_file, 'a', encoding='utf-8')
    test_with_title = []
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data:
            idx = item['id']
            content = item['content']
            Abstract(content)
            print(idx)
            Title(bert_model)
            title_file = open("out-title.txt", encoding='utf-8')
            title_str = title_file.read()
            title = title_str  # 你的模型预测title
            test_with_title.append({"id": idx, "title": title, "content": content})
    jst = json.dumps(test_with_title, ensure_ascii=False)
    fw.write(jst)


if __name__ == '__main__':
    # 官方发布的测试数据
    input_file = 'test_no_title.json'
    # 提交的测试集结果
    # 邮件只上传   团队编号_队伍名称_队长姓名.json文件
    output_file = '94012439-你们不要再打啦-王唯一.json'
    read_and_write_data(input_file, output_file)

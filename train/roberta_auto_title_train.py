# -*- coding: utf-8 -*-
import torch
from tqdm import tqdm
import time
from torch.utils.data import Dataset, DataLoader
from bert_seq2seq import Tokenizer, load_chinese_base_vocab
from bert_seq2seq import load_bert

vocab_path = "./state_dict/roberta/roberta_wwm_vocab.txt"  # roberta模型字典的位置
word2idx = load_chinese_base_vocab(vocab_path, simplfied=False)
model_name = "roberta"  # 选择模型名字
model_path = "./state_dict/roberta/roberta_wwm_pytorch_model.bin"  # 模型位置
model_save_path = "./state_dict/bert_textrank_auto_title_model.bin"
batch_size = 16  # 原来是16，改小一点
lr = 1e-5
maxlen = 256


def read_file(src_dir, tgt_dir):
    src = []
    tgt = []
    with open(src_dir, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            src.append(line.strip('\n').lower())
    with open(tgt_dir, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            tgt.append(line.strip('\n').lower())
    return src, tgt


class BertDataset(Dataset):
    def __init__(self, sents_src, sents_tgt):
        ## 一般init函数是加载所有数据
        super(BertDataset, self).__init__()
        self.sents_src = sents_src
        self.sents_tgt = sents_tgt
        self.idx2word = {k: v for v, k in word2idx.items()}
        self.tokenizer = Tokenizer(word2idx)

    def __getitem__(self, i):
        ## 得到单个数据
        print(i)
        src = self.sents_src[i]
        tgt = self.sents_tgt[i]
        token_ids, token_type_ids = self.tokenizer.encode(src, tgt, max_length=maxlen)
        output = {
            "token_ids": token_ids,
            "token_type_ids": token_type_ids,
        }
        return output

    def __len__(self):
        return len(self.sents_src)


def collate_fn(batch):
    def padding(indice, max_length, pad_idx=0):
        pad_indice = [item + [pad_idx] * max(0, max_length - len(item)) for item in indice]
        return torch.tensor(pad_indice)

    token_ids = [data["token_ids"] for data in batch]
    max_length = max([len(t) for t in token_ids])
    token_type_ids = [data["token_type_ids"] for data in batch]
    token_ids_padded = padding(token_ids, max_length)
    token_type_ids_padded = padding(token_type_ids, max_length)
    target_ids_padded = token_ids_padded[:, 1:].contiguous()
    return token_ids_padded, token_type_ids_padded, target_ids_padded


class Trainer:
    def __init__(self):
        # 加载数据
        # src_dir = './corpus/auto_title/train_all.src'
        # tgt_dir = './corpus/auto_title/train_all.tgt'
        src_dir = './corpus/auto_title/new_abstract.src'
        tgt_dir = './corpus/auto_title/new_title.tgt'
        self.sents_src, self.sents_tgt = read_file(src_dir, tgt_dir)
        # 判断是否有可用GPU
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print("device: " + str(self.device))
        # 定义模型
        self.bert_model = load_bert(word2idx, model_name=model_name, model_class="seq2seq")
        self.bert_model.set_device(self.device)
        ## 加载预训练的模型参数
        self.bert_model.load_pretrain_params(model_path)
        # 声明需要优化的参数
        self.optim_parameters = list(self.bert_model.parameters())
        self.optimizer = torch.optim.Adam(self.optim_parameters, lr=lr, weight_decay=1e-3)
        # 声明自定义的数据加载器
        dataset = BertDataset(self.sents_src, self.sents_tgt)
        self.dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=collate_fn)

    def train(self, epoch):
        # 一个epoch的训练
        self.bert_model.train()
        self.iteration(epoch, dataloader=self.dataloader, train=True)

    def save(self, save_path):
        self.bert_model.save_all_params(save_path)
        print("{} saved!".format(save_path))

    def iteration(self, epoch, dataloader, train=True):
        total_loss = 0
        start_time = time.time()  ## 得到当前时间
        step = 0
        report_loss = 0
        for token_ids, token_type_ids, target_ids in tqdm(dataloader, position=0, leave=True):
            step += 1
            if step % 300 == 0:
                self.bert_model.eval()
                test_data = [
                    "从多次公开将病毒称为“武汉病毒”，到污蔑中国共产党和中国政治制度是“时代威胁”，再到企图将“武汉病毒”纳入G7外长会声明，蓬佩奥利用国内外各个场合对中国进行污名化攻击，制造散播“阴谋论”，其充斥冷战思维和意识形态偏见的言论令世人震惊，对当前全球抗疫合作造成严重干扰这就清楚了：疫情发生后，蓬佩奥之所以屡屡攻击中国，就是企图捞取政治资本，在美国越来越充满不确定性的多方政治角力中牟取最大私利，以图实现政治野心观察人士评价说，蓬佩奥把他主政美国中情局时那套“撒谎、欺骗和盗窃”的把戏带到外交舞台上，正在加剧美国在全球的孤立局面，也给美国抗疫造成更大困难",
                    "战“疫”任务重、压力大、持续时间长，更需要给广大基层干部降压减负，让他们轻装上阵，绝不能让无谓的督查检查耗散他们的精力，干扰防控工作新华社北京2月14日电 当前，疫情防控工作到了最吃劲的关键阶段，为有效推动战“疫”，适当开展督查检查有其必要性在抗击疫情的特殊时期，更需要用好督查检查这个利器推动防控任务落地见效",
                    "“绿水青山就是金山银山”的理念，为我们平衡发展和环保的关系提供了思想指引和行动指南，不仅引领中国走出了一条兼顾经济与生态的新路子，也为其他发展中国家提供了有益借鉴这一理念的创造性就在于，它不是用排他性的眼光来看待经济发展和环境保护之间的关系，而是在绿水青山和金山银山之间打开一条通道，指出了一种兼顾经济与生态、开发与保护的发展新路径强调“绿水青山就是金山银山”，就是要尽最大可能维持经济发展与生态环境之间的精细平衡，走生态优先、绿色发展的路子，形成包括绿色消费、绿色生产、绿色流通、绿色金融等在内的完整绿色经济体系"]
                for text in test_data:
                    print(self.bert_model.generate(text, beam_size=3))
                print("loss is " + str(report_loss))
                report_loss = 0
                # self.eval(epoch)
                self.bert_model.train()
            if step % 8000 == 0:
                self.save(model_save_path)
            # 因为传入了target标签，因此会计算loss并且返回
            predictions, loss = self.bert_model(token_ids,
                                                token_type_ids,
                                                labels=target_ids,
                                                )
            report_loss += loss.item()
            # 反向传播
            if train:
                # 清空之前的梯度
                self.optimizer.zero_grad()
                # 反向传播, 获取新的梯度
                loss.backward()
                # 用获取的梯度更新模型参数
                self.optimizer.step()
            # 为计算当前epoch的平均loss
            total_loss += loss.item()
        end_time = time.time()
        spend_time = end_time - start_time
        # 打印训练信息
        print("epoch is " + str(epoch) + ". loss is " + str(total_loss) + ". spend time is " + str(spend_time))
        # 保存模型
        self.save(model_save_path)


if __name__ == '__main__':
    trainer = Trainer()
    train_epoches = 20
    for epoch in range(train_epoches):
        # 训练一个epoch
        trainer.train(epoch)

'''
测试标题：
进入“重大灾难期”的美国，蓬佩奥们为何趁火打劫？
辛识平别让“督查泛滥”拖累基层战“疫”
绿水青山就是金山银山
'''

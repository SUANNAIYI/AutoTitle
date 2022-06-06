import json
import summarization_extraction_textrank4zh
f = open('../data/dev.json', encoding='utf-8')
data = json.load(f)
f.close()
for i in range(0, 100):
    item = data[i]
    with open('temp.src', 'w', encoding='utf-8') as src:
        src.write(item['content'])
    with open('temp.src', 'r', encoding='utf-8') as njuptcs:
        text = njuptcs.read().replace('\n', '')
    summarize_text = summarization_extraction_textrank4zh.getSummary(text)
    with open('test_abstract.src', 'a', encoding='utf-8') as abstract:
        for n in summarize_text:
            abstract.write(n)
        abstract.write('\n')
    with open('test_title.tgt', 'a', encoding='utf-8') as tgt:
        tgt.write(item['title'] + '\n')

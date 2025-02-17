import json
from tqdm import tqdm
from collections import Counter
import ipdb
import os

counter = []
acc = []
filtered_data = {}
for file in os.listdir('output'):
    path = os.path.join('output', file)
    with open(path) as f:
        data_ = json.load(f)
        main_ = data_['conv'][0]['content']
        main_ = main_.split('[begin of conversation]')[-1]
        main_ = main_.split('[end of conversation]')[0]
        data_['query'] = main_

        winner = data_['raw_data'][1]
        data = data_['conv'][-1]['content']
        if data:
            data = data.split('\n')[-1]
            if 'A' in data:
                counter.append('A')
            else:
                counter.append('B')
            if counter[-1].lower() == winner:
                acc.append(1)
                if main_ not in filtered_data:
                    filtered_data[main_] = {}
                filtered_data[main_][data_['raw_data'][-1]] = data_
            else:
                acc.append(0)

print(Counter(counter).most_common())
print(acc.count(1)/len(acc))

new_counter = []
assert len(counter) == len(acc)
for c, a in zip(counter, acc):
    if a == 1:
        new_counter.append(c)

print(Counter(new_counter).most_common())

##### 补充 domain 数据
file = '../multicritique_sft/train.jsonl'
pbar = tqdm(total=64804)
with open(file) as f:
    for line in f:
        item = json.loads(line)
        ipt = item['input']
        query_ipt = '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in ipt])
        if query_ipt in filtered_data:
            filtered_data[query_ipt]['key_name'] = item['key_name']
            filtered_data[query_ipt]['dataset_name'] = item['dataset']
        pbar.update(1)

with open('filtered_data_processed.json', 'w') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)


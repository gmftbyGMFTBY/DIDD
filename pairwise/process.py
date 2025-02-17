import json
from itertools import chain
from copy import deepcopy
import re
import random
from tqdm import tqdm
import os
from collections import Counter
import ipdb



def remove_labels(string):
    new_string = re.sub(r'\[S\d+\]', '', string)
    return new_string

def convert(item):
    conversation_input = '\n'.join([f'["Begin of Utterance"] {utterance["role"]}: {utterance["content"]} [End of Utterance]' for utterance in item['input'] + [{'role': 'assistant', 'content': item['response']}]])
    conversation = [{'input': conversation_input, 'output': item['critique'][-1]}]
    return conversation


if __name__ == "__main__":
    random.seed(0)

    file = '../multicritique_sft/train.jsonl'

    pbar = tqdm(total=64804)
    new_data = {}
    with open(file) as f:
        for line in f:
            item = json.loads(line)
            string = '\n'.join([utterance['content'] for utterance in item['input']])
            if string not in new_data:
                new_data[string] = {}

            quality = item['evaluated_response_quality']
            ipt = item['input']
            response = item['responses'][quality]
            critique = item['parse_final_feedbacks']
            score = item['parse_final_judgement_score']
            new_data[string][quality] = {
                'input': ipt,
                'response': response,
                'critique': critique,
                'score': score
            }
            pbar.update(1)
            ipdb.set_trace()

    processed_data = {}
    for key, value in new_data.items():
        if len(value) == 3 and 'low' in value and 'medium' in value and 'high' in value:
            low_score = value['low']['score']
            medium_score = value['medium']['score']
            high_score = value['high']['score']
            if low_score < medium_score < high_score:
                processed_data[key] = value

    print(len(processed_data))

    with open('filtered_data.json', 'w') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

    exit()

    print({key: len(value) for key, value in new_data.items()})

    small_train_data, train_data = {}, {}
    supply_train_data = {}
    for key in new_data:
        indexes = random.sample(range(len(new_data[key])), min(base_num, len(new_data[key])))
        train_data[key] = [new_data[key][index] for index in indexes] # 每条数据 200 -> 2000条

        small_samples = random.sample(train_data[key], min(small_base_num, len(train_data[key])))
        small_train_data[key] = small_samples

        indexes = set(range(len(new_data[key]))) - set(indexes)
        indexes = list(indexes)
        supply_samples_indexes = random.sample(indexes, min(supply_base_num, len(indexes)))
        supply_samples = [new_data[key][index] for index in supply_samples_indexes]
        supply_train_data[key] = supply_samples
        print(f'{key} - {len(train_data[key])}; {len(small_train_data[key])}; {len(supply_train_data[key])}')

    with open('data/baseline_data.json', 'w') as f:
        train_data = list(chain(*[train_data[key] for key in train_data]))
        json.dump(train_data, f, ensure_ascii=False, indent=4)
        print(f'[!] save {len(train_data)} samples into baseline_data.json')

    for i in range(2, 9):
        with open(f'data/supply_train_data_score_{i}.json', 'w') as f:
            json.dump(supply_train_data[i], f, ensure_ascii=False, indent=4)
        print(f'[!] save {len(supply_train_data[i])} samples into supply_train_data[{i}].json')

    # 0, 200, 400, 800, 1000
    small_train_data = list(chain(*[small_train_data[key] for key in small_train_data]))
    for i in range(2, 9):
        supply_data = supply_train_data[i]
        for num in [200, 400, 800, 1000]:
            nn = deepcopy(small_train_data)
            nn.extend(supply_data[:num])
            with open(f'data/papo_score_{i}_num_{num}.json', 'w') as f:
                json.dump(nn, f, ensure_ascii=False, indent=4)
            print(f'[!] save {len(nn)} samples into papo_score_{i}_num_{num}.json')

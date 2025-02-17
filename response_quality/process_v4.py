import json
from itertools import chain
from copy import deepcopy
import re
import random
from tqdm import tqdm
import os
from collections import Counter
import ipdb

'''overall 中 medium 比例高一些（主观分数显示 medium 多了主观会高）
且 medium 改为4<= <=6: medium_v4.json
overall_v3.json
'''


def remove_labels(string):
    new_string = re.sub(r'\[S\d+\]', '', string)
    return new_string

def convert(item):
    conversation_input = '\n'.join([f'["Begin of Utterance"] {utterance["role"]}: {utterance["content"]} [End of Utterance]' for utterance in item['input'] + [{'role': 'assistant', 'content': item['response']}]])
    conversation = [{'input': conversation_input, 'output': item['critique'][-1]}]
    return conversation

if __name__ == "__main__":
    random.seed(0)
    prompt = open('prompts/singlewise_critique.md').read()

    file = '../multicritique_sft/train.jsonl'

    pbar = tqdm(total=64804)
    new_data = {}
    with open(file) as f:
        for line in f:
            item = json.loads(line)
            category = item['key_name']
            score = item['parse_final_judgement_score']
            score = round(score)

            if 1 <= score <= 3:
                quality = 'low'
            elif 4 <= score <= 6:
                quality = 'medium'
            else:
                quality = 'high'

            if category not in new_data:
                new_data[category] = {}
            if quality not in new_data[category]:
                new_data[category][quality] = []
            ipt = item['input']
            response = item['responses'][item['evaluated_response_quality']]
            critique = item['parse_final_feedbacks']
            score = item['parse_final_judgement_score']
            new_data[category][quality].append({
                'input': ipt,
                'response': response,
                'critique': critique,
                'score': score
            })
            pbar.update(1)

    max_base_num = 50
    d_low, d_medium, d_high = [], [], []
    for category in new_data:
        if 'low' in new_data[category]:
            # low
            samples = random.sample(new_data[category]['low'], min(max_base_num, len(new_data[category]['low'])))
            d_low.extend(samples)

        if 'medium' in new_data[category]:
            # medium 
            samples = random.sample(new_data[category]['medium'], min(max_base_num, len(new_data[category]['medium'])))
            d_medium.extend(samples)

        if 'high' in new_data[category]:
            # high 
            samples = random.sample(new_data[category]['high'], min(max_base_num, len(new_data[category]['high'])))
            d_high.extend(samples)

    print(f"low - {len(d_low)}; medium - {len(d_medium)}; high - {len(d_high)}")
    max_length = max(len(d_low), len(d_medium), len(d_high))
    rate = [0.25, 0.5, 0.25]
    num_medium, num_low, num_high = int(max_length * rate[1]), int(max_length * rate[0]), int(max_length * rate[-1])

    overall = []
    for d, num in zip([d_low, d_medium, d_high], [num_low, num_medium, num_high]):
        data = []
        for sample in random.sample(d, num):
            conv = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in sample['input']]) + ' [end of conversation]'
            string = prompt.format(conversation=conv, response=remove_labels(sample['response']))
            data.append({'conversation': [{'input': string, 'output': sample['critique'][-1]}]})
        overall.extend(data)
    print(f'[!] overall:', len(overall))

    new_datasets = []
    for d, file_name in zip([d_medium], ['data/medium_v4.json']):
        data = []
        for sample in d:
            conv = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in sample['input']]) + ' [end of conversation]'
            string = prompt.format(conversation=conv, response=remove_labels(sample['response']))
            data.append({'conversation': [{'input': string, 'output': sample['critique'][-1]}]})
        with open(file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f'[!] {file_name}:', len(data))

    with open('data/overall_v3.json', 'w') as f:
        json.dump(overall, f, ensure_ascii=False, indent=4)

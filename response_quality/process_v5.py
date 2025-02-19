import json
from itertools import chain
from copy import deepcopy
import re
import random
from tqdm import tqdm
import os
from collections import Counter
import ipdb

'''
固定 medium 比例为0.5，测试 high:low的比例和效果的对比：
high:low=10:0
high:low=9:1
high:low=8:2
high:low=7:3
high:low=6:4
high:low=5:5
high:low=4:6
high:low=3:7
high:low=2:8
high:low=1:9
high:low=0:10
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
    #max_length = max(len(d_low), len(d_medium), len(d_high))
    medium_set = random.sample(d_medium, 1500)
    max_base_num = 1500 # high + low

    for high_rate in [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]:
        low_rate = 1 - high_rate
        high_rate, low_rate = round(high_rate, 1), round(low_rate, 1)
        num_low, num_high = int(low_rate * max_base_num), int(high_rate * max_base_num)
        low_set = random.sample(d_low, num_low)
        high_set = random.sample(d_high, num_high)
        overall = []
        for sample in medium_set + low_set + high_set:
            conv = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in sample['input']]) + ' [end of conversation]'
            string = prompt.format(conversation=conv, response=remove_labels(sample['response']))
            overall.append({'conversation': [{'input': string, 'output': sample['critique'][-1]}]})
        with open(f'data/high_vs_low_exp_{high_rate}_{low_rate}.json', 'w') as f:
            json.dump(overall, f, ensure_ascii=False, indent=4)
        print(f'[!] high-vs-low: {high_rate}-{low_rate}; high-num-{num_high}-low-num-{num_low}-overall-{len(overall)}')

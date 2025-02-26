import json
from itertools import chain
from copy import deepcopy
import re
import random
from tqdm import tqdm
import os
from collections import Counter
import ipdb

'''随机采样 1000,2000,3000,4000,5000,6000,7000,8000 样本'''


def remove_labels(string):
    new_string = re.sub(r'\[S\d+\]', '', string)
    return new_string

if __name__ == "__main__":
    random.seed(0)
    prompt = open('prompts/singlewise_critique.md').read()

    file = '../multicritique_sft/train.jsonl'
    pbar = tqdm(total=64804)
    new_data = []
    with open(file) as f:
        for line in f:
            item = json.loads(line)
            category = item['key_name']
            score = item['parse_final_judgement_score']
            score = round(score)
            ipt = item['input']
            response = item['responses'][item['evaluated_response_quality']]
            critique = item['parse_final_feedbacks']
            score = item['parse_final_judgement_score']
            new_data.append({
                'input': ipt,
                'response': response,
                'critique': critique,
                'score': score
            })
            pbar.update(1)

    for sample_num in [1000, 2000, 4000, 7000, 8000]:
        subdata = random.sample(new_data, sample_num)
        data = []
        for sample in subdata:
            conv = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in sample['input']]) + ' [end of conversation]'
            string = prompt.format(conversation=conv, response=remove_labels(sample['response']))
            data.append({'conversation': [{'input': string, 'output': sample['critique'][-1]}]})
        file_name = f'data/baseline_{sample_num}.json'
        with open(file_name, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f'[!] {file_name}:', len(data))

import json
from copy import deepcopy
from tqdm import tqdm
from itertools import chain
import os
import ipdb
import sys
import argparse
from utils import *
import re


def remove_labels(string):
    new_string = re.sub(r'\[S\d+\]', '', string)
    return new_string

def packup_examples(examples):
    prompt_string = '''# 样例 {index}\n## Query: {query}\n## Response: {response}'''
    strings = []
    for index, example in enumerate(examples):
        ipt = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in example['input']]) + ' [end of conversation]'
        example_string = prompt_string.format(query=ipt, response=remove_labels(example['response']), index=index)
        strings.append(example_string)
    return '\n'.join(strings)


def generate_test_data(few_shot):
    '''step 1: 生成测试数据，检验模型的效果'''
    random.seed(0)
    dataset = []
    for category, value in few_shot.items():
        samples = list(chain(*[value[q] for q in value]))
        examples = random.sample(samples, min(5, len(samples)))
        reference = packup_examples(examples)
        prompt_string = prompt.format(
            abbr=category,
            reference=reference
        )
        dataset.append((prompt_string, category))
    return dataset


def batch_chat_with_api(dataset, output_path):
    bsz = 16
    if os.path.exists(output_path) is False:
        os.makedirs(output_path)

    # load cached rest
    cached = []
    for file in os.listdir(output_path):
        if file.endswith('json'):
            cached.append(file)
    cache_num = len(cached)
    print(f'[!] load {cache_num} cached samples')

    # load prompt
    for index in tqdm(range(0, len(dataset[cache_num:]), bsz)):
        samples_ = dataset[cache_num+index:cache_num+index+bsz]
        batch = []
        for prompt_string, category in samples_:
            batch.append([{'role': 'user', 'content': prompt_string}])
        responses = batch_chat(batch)
        assert len(batch) == len(responses)
        for j, (s, b, r) in enumerate(list(zip(samples_, batch, responses))):
            b.append({'role': 'assistant', 'content': r})
            b.append(s[1])
            with open(os.path.join(output_path, str(cache_num+index+j) + '.json'), 'w') as f:
                json.dump(b, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    prompt = open('prompts/detail.md').read()
    few_shot = json.load(open('few_shot.json'))
    test_set = generate_test_data(few_shot)
    batch_chat_with_api(test_set, f'data')



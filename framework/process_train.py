import json
from itertools import chain
from copy import deepcopy
import re
import random
from tqdm import tqdm
import os
from collections import Counter
import ipdb
import sys
sys.path.append('gpt4_generation')
from data_generation import parse_test_set



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

    baseline_data = json.load(open('data/baseline.json'))
    print(f'[!] baseline data:', len(baseline_data))

    iter_data = 'gpt4_generation/debug/iter_0/train_set_gn_50_fsn_3'
    for file in os.listdir(iter_data):
        path = os.path.join(iter_data, file)
        sample = json.load(open(path))
        # parse the sample
        gen_sample = parse_test_set(sample)
        for sample in gen_sample:
            input = [{'role': 'user', 'content': sample['query']}]
            ipt = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in input]) + ' [end of conversation]'
            string = prompt.format(conversation=ipt, response=sample['response'])
            conv = {'conversation': [{'input': string, 'output': sample['critique']}]}
            baseline_data.append(conv)
    print(f'[!] overall baseline data:', len(baseline_data))

    with open('data/baseline_iter_0_v2.json', 'w') as f:
        json.dump(baseline_data, f, ensure_ascii=False, indent=4)

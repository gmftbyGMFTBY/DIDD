import json
import numpy as np
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

if __name__ == "__main__":
    random.seed(0)
    prompt = open('prompts/singlewise_critique.md').read()

    #baseline_data = json.load(open('data/baseline.json'))
    #baseline_data = json.load(open('data/ultracm_ours.json'))
    #baseline_data = json.load(open('data/autoj_ours.json'))

    modes = ['raw', 'new']

    iter_data = [
        'gpt4_generation/data_baseline_20250218/iter_0/train_set_gn_20_fsn_3',
    ]
    for mode in modes:
        baseline_data = json.load(open('data/baseline.json'))
        print(f'[!] baseline data:', len(baseline_data))
        avg_num = []
        for iter_path in iter_data:
            iter_path = iter_path + f'_mode_{mode}'
            for file in os.listdir(iter_path):
                path = os.path.join(iter_path, file)
                sample = json.load(open(path))
                # parse the sample
                gen_sample = parse_test_set(sample)
                avg_num.append(len(gen_sample))
                for sample in gen_sample:
                    input = [{'role': 'user', 'content': sample['query']}]
                    ipt = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in input]) + ' [end of conversation]'
                    string = prompt.format(conversation=ipt, response=sample['response'])
                    conv = {'conversation': [{'input': string, 'output': sample['critique']}]}
                    baseline_data.append(conv)
        print(f'[!] {mode} overall baseline data:', len(baseline_data))
        print(f'[!] avg generation:', np.mean(avg_num))

        with open(f'data/baseline_iter_0_mode_{mode}.json', 'w') as f:
            json.dump(baseline_data, f, ensure_ascii=False, indent=4)

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

if __name__ == "__main__":
    random.seed(0)
    prompt = open('prompts/singlewise_critique.md').read()

    baseline_data = json.load(open('data/baseline.json'))
    iter_path = 'gpt4_generation/data_baseline_20250218/iter_0/train_set_gn_400_20_fsn_3_mode_mixture_rate_0.6'
    print(f'[!] baseline data:', len(baseline_data))
    new_data = []
    for file in os.listdir(iter_path):
        path = os.path.join(iter_path, file)
        sample = json.load(open(path))
        # parse the sample
        gen_sample = parse_test_set(sample)
        for sample in gen_sample:
            input = [{'role': 'user', 'content': sample['query']}]
            ipt = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in input]) + ' [end of conversation]'
            string = prompt.format(conversation=ipt, response=sample['response'])
            conv = {'conversation': [{'input': string, 'output': sample['critique']}]}
            new_data.append(conv)
    print(f'[!] overall parsed data:', len(new_data))
    nums = [200, 400, 1000, len(new_data)]
    for num in nums:
        with open(f'data/baseline_data_iter_0_mixture_rate_0.6_train_num_{num}.json', 'w') as f:
            samples = baseline_data + random.sample(new_data, num)
            json.dump(samples, f, ensure_ascii=False, indent=4)
            print(f'[!] save samples:', len(samples))


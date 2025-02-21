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

    for test_num in [200, 800, 1000]:
        baseline_data = json.load(open('data/baseline.json'))
        print(f'[!] baseline data:', len(baseline_data))
        iter_path = f'gpt4_generation/data_baseline_20250218_test_num_{test_num}/iter_0/train_set_gn_20_fsn_3_mode_mixture_rate_0.5'
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
                baseline_data.append(conv)
        print(f'[!] overall baseline data:', len(baseline_data))
        with open(f'data/baseline_test_num_{test_num}_iter_0.json', 'w') as f:
            json.dump(baseline_data, f, ensure_ascii=False, indent=4)

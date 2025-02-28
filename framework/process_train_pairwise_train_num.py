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
sys.path.append('gpt4_generation_pairwise')
from data_generation import parse_test_set



def remove_labels(string):
    new_string = re.sub(r'\[S\d+\]', '', string)
    return new_string

if __name__ == "__main__":
    random.seed(0)
    prompt = open('prompts/pairwise_critique.md').read()

    #baseline_data = json.load(open('../pairwise/data/overall.json'))
    #baseline_data = json.load(open('../pairwise/data/hard_2.json'))
    #print(f'[!] baseline data:', len(baseline_data))
 
    # 为了只训练iter_1数据
    iter_data = [
        '/home/lt/ReNewPoNe/framework/gpt4_generation_pairwise/data_baseline_overall_dis_20250218/iter_0/train_set_gn_400_10_fsn_3_mode_mixture_rate_0.6'
    ]
    baseline_data = []
    for iter_path in iter_data:
        for file in os.listdir(iter_path):
            path = os.path.join(iter_path, file)
            sample = json.load(open(path))
            # parse the sample
            gen_sample = parse_test_set(sample)
            for sample in gen_sample:
                input = [{'role': 'user', 'content': sample['query']}]
                ipt = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in input]) + ' [end of conversation]'
                string = prompt.format(conversation=ipt, responsea=sample['responsea'], responseb=sample['responseb'])
                conv = {'conversation': [{'input': string, 'output': sample['critique']}]}
                baseline_data.append(conv)
        print(f'[!] overall baseline data:', len(baseline_data))
    for num in [200, 400, 800, 1000, 2000, 4000]:
        samples = random.sample(baseline_data, min(num, len(baseline_data)))
        with open(f'data/comp_iter_train_num_{num}.json', 'w') as f:
            json.dump(samples, f, ensure_ascii=False, indent=4)
        print(f'[!] {len(samples)}')

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
        ('/home/lt/ReNewPoNe/framework/gpt4_generation_pairwise/data_baseline_easy_test_num_20250224_test_num_100/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.5', 100),
        ('/home/lt/ReNewPoNe/framework/gpt4_generation_pairwise/data_baseline_easy_test_num_20250224_test_num_200/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.5', 200),
        ('/home/lt/ReNewPoNe/framework/gpt4_generation_pairwise/data_baseline_easy_test_num_20250224_test_num_400/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.5', 400),
        ('/home/lt/ReNewPoNe/framework/gpt4_generation_pairwise/data_baseline_easy_test_num_20250224_test_num_500/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.5', 500),
        ('/home/lt/ReNewPoNe/framework/gpt4_generation_pairwise/data_baseline_easy_test_num_20250224_test_num_800/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.5', 800),
        ('/home/lt/ReNewPoNe/framework/gpt4_generation_pairwise/data_baseline_easy_test_num_20250224_test_num_1000/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.5', 1000),
    ]
    for iter_path, num in iter_data:
        baseline_data = []
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
        with open(f'data/pairwise_test_num_scaling_{num}.json', 'w') as f:
            json.dump(baseline_data, f, ensure_ascii=False, indent=4)
        print(f'[!] {len(baseline_data)}')

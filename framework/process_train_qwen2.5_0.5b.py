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
    print(f'[!] baseline data:', len(baseline_data))

    iter_data = [
        #'gpt4_generation/data_baseline_llama3_8b_20250218/iter_0/train_set_gn_20_fsn_3_mode_mixture_rate_0.5',
        #"/home/lt/ReNewPoNe/framework/gpt4_generation/data_qwen2.5_0.5B_20250715/iter_0/train_set_gn_100_10_fsn_2_mode_mixture_rate_0.8"
        #"/home/lt/ReNewPoNe/framework/gpt4_generation/data_qwen2.5_0.5B_20250715_v2/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.6"
        #"/home/lt/ReNewPoNe/framework/gpt4_generation/data_qwen2.5_1.5B_20250715/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.6"
        #"/home/lt/ReNewPoNe/framework/gpt4_generation/data_qwen2.5_3B_20250715/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.6"
        #"/home/lt/ReNewPoNe/framework/gpt4_generation/data_qwen2.5_7B_20250715/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.6"
        #
        #
        #"/home/lt/ReNewPoNe/framework/gpt4_generation/data_qwen2_0.5B_20250715/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.6"
        "/home/lt/ReNewPoNe/framework/gpt4_generation_pairwise/data_revision_20250715_qwen2_5_1_5B/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.5"
    ]
    for iter_path in iter_data:
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
    with open('data/qwen2-1.5b_iter_0.json', 'w') as f:
        json.dump(baseline_data, f, ensure_ascii=False, indent=4)

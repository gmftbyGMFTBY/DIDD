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
    #for num in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]:
    iter_data = [
        #'gpt4_generation_pairwise/data_20250224_new_resquality_dis_from_hard_2/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.5'
        #f'gpt4_generation_pairwise/data_baseline_easy_test_num_20250224_test_num_{num}/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.5'
        #'gpt4_generation_pairwise/data_20250225_hard_2_balance_ab/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.5'
        #'gpt4_generation/data_mixture_rate_06_8508_iter_1/iter_1/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.6'
        #'gpt4_generation_pairwise/data_baseline_20250226_llama3_base_model/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.5'
        #'gpt4_generation_pairwise/data_baseline_20250227_llama3_data_on_internlm/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.9'
        #### iter_exp
        #'gpt4_generation_pairwise/iter_exp_20250227/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.4',
        #'gpt4_generation_pairwise/iter_exp_20250227/iter_1/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.4',
        #'gpt4_generation_pairwise/iter_exp_20250227/iter_2/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.4'
        #### iter_exp_v2
        "gpt4_generation_pairwise/iter_exp_20250227_v2/iter_0/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.4",
        "gpt4_generation_pairwise/iter_exp_20250227_v2/iter_1/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.4",
        "gpt4_generation_pairwise/iter_exp_20250227_v2/iter_2/train_set_gn_100_10_fsn_3_mode_mixture_rate_0.4"
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
    with open(f'data/comp_iter_012_v2_only.json', 'w') as f:
        json.dump(baseline_data, f, ensure_ascii=False, indent=4)

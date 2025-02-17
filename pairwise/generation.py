import json
from copy import deepcopy
from tqdm import tqdm
from itertools import chain
import os
import ipdb
import sys
import argparse
from utils import *

parser = argparse.ArgumentParser()
parser.add_argument("--data-path", default='filtered_data.json')
parser.add_argument("--output-path", default='output')
parser.add_argument("--bsz", default=16, type=int)
parser.add_argument("--random_seed", default=0, type=float)
args = parser.parse_args()


prompt = open('prompts/pairwise_critique.md').read()


if __name__ == "__main__":
    random.seed(args.random_seed)
    with open(args.data_path) as f:
        data = json.load(f)

    samples = []
    for key, value in data.items():
        ipt = value['low']['input']
        ipt = '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in ipt])
        ipt = '[begin of conversation]' + ipt + '[end of conversation]'

        response_low = value['low']['response']
        response_medium = value['medium']['response']
        response_high = value['high']['response']

        if random.random() < 0.5:
            response_a, response_b = response_low, response_high
            winner = 'b'
        else:
            response_a, response_b = response_high, response_low
            winner = 'a'
        prompt_string = prompt.format(conversation=ipt, responsea=response_a, responseb=response_b)
        samples.append((prompt_string, winner, 'low-high'))

        if random.random() < 0.5:
            response_a, response_b = response_low, response_medium
            winner = 'b'
        else:
            response_a, response_b = response_medium, response_low
            winner = 'a'
        prompt_string = prompt.format(conversation=ipt, responsea=response_a, responseb=response_b)
        samples.append((prompt_string, winner, 'low-medium'))

        if random.random() < 0.5:
            response_a, response_b = response_medium, response_high
            winner = 'b'
        else:
            response_a, response_b = response_high, response_medium
            winner = 'a'
        prompt_string = prompt.format(conversation=ipt, responsea=response_a, responseb=response_b)
        samples.append((prompt_string, winner, 'medium-high'))

    if os.path.exists(args.output_path) is False:
        os.makedirs(args.output_path)

    # load cached rest
    cached = []
    for file in os.listdir(args.output_path):
        if file.endswith('json'):
            cached.append(file)
    cache_num = len(cached)
    print(f'[!] load {cache_num} cached samples')

    # load prompt
    for index in tqdm(range(0, len(samples[cache_num:]), args.bsz)):
        samples_ = samples[cache_num+index:cache_num+index+args.bsz]
        batch = []
        for prompt_string, winner, mode in samples_:
            batch.append([{'role': 'user', 'content': prompt_string}])
        responses = batch_chat(batch)
        assert len(batch) == len(responses) == len(samples_)
        for j, (s, b, r) in enumerate(list(zip(samples_, batch, responses))):
            b.append({'role': 'assistant', 'content': r})

            new_item = {
                'conv': b,
                'raw_data': s, 
            }
            with open(os.path.join(args.output_path, str(cache_num+index+j) + '.json'), 'w') as f:
                json.dump(new_item, f, ensure_ascii=False, indent=4)

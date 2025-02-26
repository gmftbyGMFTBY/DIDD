import json
import numpy as np
from copy import deepcopy
from tqdm import tqdm
from itertools import chain
import os
import ipdb
import sys
import argparse
from utils import *
from collections import Counter
import re

from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig, ChatTemplateConfig
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, AutoConfig, AutoModel, LlamaTokenizer, LlamaForCausalLM
from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig

def parse_test_set(sample):
    gen = sample[-1]['content']
    if gen is None:
        return []
    if 'markdown' in gen:
        samples = re.findall(r'```markdown\n(.+)```', gen, re.DOTALL | re.MULTILINE)
        try:
            assert len(samples) == 1
        except:
            return []
    else:
        samples = [gen]
    examples = re.split(r'.*# Data \d', samples[0])
    examples = [example.strip() for example in examples if example.strip()]

    gen_results = []
    for example in examples:
        query = re.findall(r'## Query:(.+)## Response', example, re.DOTALL | re.MULTILINE)
        responsea = re.findall(r'## Response_A:(.+)## Response_B', example, re.DOTALL | re.MULTILINE)
        responseb = re.findall(r'## Response_B:(.+)## Critique', example, re.DOTALL | re.MULTILINE)
        critique = re.findall(r'## Critique:(.+)', example, re.DOTALL | re.MULTILINE)
        try:
            assert len(query) == 1 and len(responsea) == 1 and len(responseb) == 1 and len(critique) == 1
        except:
            continue
        query, responsea, responseb, critique = query[0], responsea[0], responseb[0], critique[0]
        gen_results.append({
            'query': query,
            'responsea': responsea,
            'responseb': responseb,
            'critique': critique
        })
    return gen_results


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


def generate_train_data(few_shot, few_shot_def, domain):
    dataset = []
    samples = list(chain(*[few_shot[key] for key in few_shot]))
    for _ in range(50):
        examples = random.sample(samples, 3)
        reference = packup_examples(examples)
        if random.random() < 0.5:
            good_response = 'A'
        else:
            good_response = 'B'
        prompt_string = prompt.format(
            domain=domain,
            generationnum=10,
            reference=reference,
            domaindef=few_shot_def,
            good_response=good_response
        )
        dataset.append(prompt_string)
    return dataset

    
def batch_chat_with_api_train(dataset, output_path):
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
    for index in tqdm(range(0, len(dataset[cache_num:]), 16)):
        samples_ = dataset[cache_num+index:cache_num+index+16]
        batch = []
        for prompt_string in samples_:
            batch.append([{'role': 'user', 'content': prompt_string}])
        responses = batch_chat(batch)
        assert len(batch) == len(responses)
        for j, (s, b, r) in enumerate(list(zip(samples_, batch, responses))):
            b.append({'role': 'assistant', 'content': r})
            with open(os.path.join(output_path, str(cache_num+index+j) + '.json'), 'w') as f:
                json.dump(b, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    prompt = open('prompts/data_generation_v2_pairwise.md').read()
    few_shot = json.load(open('new_few_shot.json'))
    few_shot_detail = json.load(open('few_shot_detail_v2.json'))

    domain_dis = [
        'general_communication',
        'creative_writing',
        'nlp_tasks',
        'summarization',
        'code',
        'exam_question',
        'functional_writing',
        'rewriting'
    ]

    for domain in tqdm(domain_dis):
        train_set = generate_train_data(few_shot[domain], few_shot_detail[domain], domain)
        subfolder_name = f'output/{domain}'
        if os.path.exists(subfolder_name) is False:
            os.makedirs(subfolder_name)
        batch_chat_with_api_train(train_set, subfolder_name)

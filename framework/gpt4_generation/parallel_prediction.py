import json
from copy import deepcopy
from tqdm import tqdm
from itertools import chain
import os
import ipdb
import sys
import argparse
from utils import *
import re

from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig, ChatTemplateConfig
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, AutoConfig, AutoModel, LlamaTokenizer, LlamaForCausalLM
from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig

parser = argparse.ArgumentParser()
# test_set_construction, evaluate
parser.add_argument("--mode", default='test_set_construction')
parser.add_argument("--model-prompt", default='')
parser.add_argument("--model-prediction-name", default='')
parser.add_argument("--model-path", default='')
parser.add_argument("--model-bsz", default=16, type=int)
parser.add_argument("--failure-dis-file", default='')
parser.add_argument("--root-path", default='output')
parser.add_argument("--bsz", default=16, type=int)
parser.add_argument("--gen-num", default=16, type=int)
parser.add_argument("--random_seed", default=0, type=float)
parser.add_argument("--few-shot-num", default=3, type=int)
parser.add_argument("--iter-num", default=0, type=int)
parser.add_argument("--train-num-each", default=0, type=int)
args = parser.parse_args()


"""distribution 分布：
1. 初始的distribution是 uniform 每一个都采样：113 * 3 * 5  = 1695
2. 调整后采样 top-50 个(339 -> 50) 继续采样生成：50 * 100 + 50 * 5 = 5250
"""


class OpenLLM:

    def __init__(self, model_name, prompt_file, inner_bsz):
        self.model_name = model_name
        backend_config = PytorchEngineConfig(session_len=32768, tp=1)
        self.gen_config = GenerationConfig(temperature=0.0, max_new_tokens=4096)
        self.pipe = pipeline(model_name, backend_config=backend_config, chat_template_config=ChatTemplateConfig(model_name="internlm2"))
        self.prompt = open(prompt_file).read()
        self.inner_bsz = inner_bsz

    def prepare_prompt(self, msg):
        string = self.prompt.format(conversation=msg[0]['query'], response=msg[0]['response'])
        return string

    @torch.no_grad()
    def batch_chat(self, msgs, max_new_tokens=2048):
        index = 0
        pbar = tqdm(total=len(msgs))
        outputs = []
        while index < len(msgs):
            msgs_ = [self.prepare_prompt(msg) for msg in msgs[index:index+self.inner_bsz]]
            responses = self.pipe(msgs_, gen_config=self.gen_config)
            responses = [response.text for response in responses]
            index += self.inner_bsz
            outputs.extend(responses)
            pbar.update(len(msgs_))

        new_outputs = []
        assert len(outputs) == len(msgs)
        for o, d in zip(outputs, msgs):
            msg, category, quality = d
            new_outputs.append({
                'raw_data': msg,
                'category': category,
                'quality': quality,
                'prediction': o

            })
        return new_outputs


def parse_test_set(sample):
    gen = sample[-1]['content']
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
        query = re.findall(r'## Query:(.+)##', example, re.DOTALL | re.MULTILINE)
        response = re.findall(r'## Response:(.+)##', example, re.DOTALL | re.MULTILINE)
        #critique = re.findall(r'## Critique:(.+)', example, re.DOTALL | re.MULTILINE)
        critique = re.findall(r'## Critique(.+)', example, re.DOTALL | re.MULTILINE)
        try:
            assert len(query) == 1 and len(response) == 1 and len(critique) == 1
        except:
            continue
        query, response, critique = query[0], response[0], critique[0]
        gen_results.append({
            'query': query,
            'response': response,
            'critique': critique
        })
    return gen_results




def remove_labels(string):
    new_string = re.sub(r'\[S\d+\]', '', string)
    return new_string


if __name__ == "__main__":
    prompt = open('prompts/data_generation.md').read()
    few_shot = json.load(open('few_shot.json'))
    few_shot_detail = json.load(open('few_shot_detail.json'))

    save_path =  f'{args.root_path}/iter_{args.iter_num}/{args.model_prediction_name}.json'
    if os.path.exists(save_path) is True:
        print(f'[!] found the generated file:', save_path)
        exit()
    model = OpenLLM(args.model_path, args.model_prompt, args.model_bsz)
    subfolder_name = f'test_set_gn_{args.gen_num}_fsn_{args.few_shot_num}'
    folder =  f'{args.root_path}/iter_{args.iter_num}/{subfolder_name}'
    test_set = []
    for file in os.listdir(folder):
        nn = file.replace('.json', '').split('_')
        index = nn[0]
        quality = nn[-1]
        category = '_'.join(nn[1:-1])
        path = os.path.join(folder, file)
        sample = json.load(open(path))
        gen_samples = parse_test_set(sample)
        test_set.extend([(a, category, quality) for a in gen_samples])
    # run the prediction of the model
    gen_results = model.batch_chat(test_set)
    save_path =  f'{args.root_path}/iter_{args.iter_num}/{args.model_prediction_name}.json'
    with open(save_path, 'w') as f:
        json.dump(gen_results, f, ensure_ascii=False, indent=4)

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

parser = argparse.ArgumentParser()
# test_set_construction, evaluate
parser.add_argument("--dis-mode", default='mixture') # mixture, new, raw
parser.add_argument("--mixture-rate", default=0.2, type=float) # mixture, new, raw
parser.add_argument("--mode", default='test_set_construction')
parser.add_argument("--model-prompt", default='')
parser.add_argument("--model-prediction-name", default='')
parser.add_argument("--model-path", default='')
parser.add_argument("--model-bsz", default=16, type=int)
parser.add_argument("--failure-dis-file", default='')
parser.add_argument("--root-path", default='output')
parser.add_argument("--bsz", default=16, type=int)
parser.add_argument("--gen-num", default=16, type=int)
parser.add_argument("--test-query-num", default=100, type=int)
parser.add_argument("--random_seed", default=0, type=float)
parser.add_argument("--few-shot-num", default=3, type=int)
parser.add_argument("--iter-num", default=0, type=int)
parser.add_argument("--train-num-each", default=0, type=int)
parser.add_argument("--train-query-num", default=0, type=int)
args = parser.parse_args()


"""distribution 分布：
1. 初始的distribution是 uniform 每一个都采样：113 * 3 * 5  = 1695
2. 调整后采样 top-50 个(339 -> 50) 继续采样生成：50 * 100 + 50 * 5 = 5250
"""


class OpenLLM:

    def __init__(self, model_name, prompt_file, inner_bsz):
        self.model_name = model_name
        backend_config = PytorchEngineConfig(session_len=32768, tp=1)
        self.gen_config = GenerationConfig(temperature=0.0, max_new_tokens=2048)
        if 'llama3' in model_name.lower():
            self.pipe = pipeline(model_name, backend_config=backend_config, chat_template_config=ChatTemplateConfig(model_name="llama3"))
        else:
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
        query = re.findall(r'## Query:(.+)## Response', example, re.DOTALL | re.MULTILINE)
        response = re.findall(r'## Response:(.+)## Critique', example, re.DOTALL | re.MULTILINE)
        critique = re.findall(r'## Critique:(.+)', example, re.DOTALL | re.MULTILINE)
        #critique = re.findall(r'## Critique(.+)', example, re.DOTALL | re.MULTILINE)
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


def packup_examples(examples):
    prompt_string = '''# 样例 {index}\n## Query: {query}\n## Response: {response}'''
    strings = []
    for index, example in enumerate(examples):
        ipt = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in example['input']]) + ' [end of conversation]'
        example_string = prompt_string.format(query=ipt, response=remove_labels(example['response']), index=index)
        strings.append(example_string)
    return '\n'.join(strings)


def generate_train_data(few_shot, domain_dis, quality_dis):
    '''step 2: 针对top-50的错误分布，生成训练数据
    使用测试数据中的样本作为 few-shot
    '''

    def choose(name, dis):
        return np.random.choice(a=name, p=dis).item()

    random.seed(args.random_seed)
    dataset = []
    selected_domains, selected_qualities = [], []
    base_ratio = args.train_num_each // 10
    domains = [a for a, b in domain_dis.items()]
    domain_dis = [b for a, b in domain_dis.items()]
    qualities = [a for a, b in quality_dis.items()]
    quality_dis = [b for a, b in quality_dis.items()]
    for _ in range(args.train_query_num):
        domain_ = choose(domains, domain_dis)
        quality_ = choose(qualities, quality_dis)
        selected_qualities.append(quality_)
        selected_domains.append(domain_)
        samples = few_shot[domain_][quality_]
        examples = random.sample(samples, min(args.few_shot_num, len(samples)))
        reference = packup_examples(examples)
        for index in range(base_ratio):
            prompt_string = prompt.format(
                responsequality=quality_,
                domain=domain_,
                generationnum=10,
                reference=reference,
                domaindef=few_shot_detail[domain_]
            )
            dataset.append((prompt_string, domain_, quality_, index))
    selected_domains = Counter(selected_domains).most_common()
    selected_qualities = Counter(selected_qualities).most_common()
    print(f'[!] domain distribution:', selected_domains)
    print(f'[!] quality distribution:', selected_qualities)
    return dataset


def generate_test_data(few_shot):
    '''step 1: 生成测试数据，检验模型的效果
    * 增大nlp_tasks, general_communication, creative_writing, summarization数据的比例
    * 增大 medium 数据的比例（4 <= x <= 6/7）
        * low: 0.1
        * medium: 0.6
        * high: 0.3
    '''

    def choose_domain(random_num):
        if 0 <= random_num < 0.175:
            return 'general_communication'
        elif 0.175 <= random_num < 0.175 * 2:
            return 'creative_writing'
        elif 0.175 * 2 <= random_num < 0.175 * 3:
            return 'nlp_tasks'
        elif 0.175 * 3 <= random_num < 0.175 * 4:
            return 'summarization'
        elif 0.175 * 3 <= random_num < 0.175 * 4:
            return 'summarization'
        elif 0.175 * 4 <= random_num < 0.175 * 4 + 0.1:
            return 'code'
        elif 0.175 * 4 + 0.1 <= random_num < 0.175 * 4 + 0.2:
            return 'exam_question'
        elif 0.175 * 4 + 0.2 <= random_num < 0.175 * 4 + 0.25:
            return 'functional_writing'
        else:
            return 'rewriting'

    def choose_quality(random_num):
        if 0 <= random_num < 0.1:
            return 'low'
        elif 0.1 <= random_num < 0.7:
            return 'medium'
        else:
            return 'high'

    random.seed(args.random_seed)
    dataset = []
    domain_dis = {
        # iter-1: 0.7
        'general_communication': 0.175,
        'creative_writing': 0.175,
        'nlp_tasks': 0.175,
        'summarization': 0.175,
        # tier-2: 0.2
        'code': 0.1,
        'exam_question': 0.1,
        # iter-3: 0.1
        'functional_writing': 0.05,
        'rewriting': 0.05,
    }
    quality_dis = {'high': 0.3, 'medium': 0.6, 'low': 0.1}
    assert sum(domain_dis.values()) == 1
    selected_domains, selected_qualities = [], []
    for _ in range(args.test_query_num):
        random_a, random_b = random.random(), random.random()
        domain_ = choose_domain(random_a)
        quality_ = choose_quality(random_b)
        selected_qualities.append(quality_)
        selected_domains.append(domain_)
        samples = few_shot[domain_][quality_]
        examples = random.sample(samples, min(args.few_shot_num, len(samples)))
        reference = packup_examples(examples)
        prompt_string = prompt.format(
            responsequality=quality_,
            domain=domain_,
            generationnum=args.gen_num,
            reference=reference,
            domaindef=few_shot_detail[domain_]
        )
        dataset.append((prompt_string, domain_, quality_))
    print(f'[!] 合成了{len(dataset)}的测试数据;每个测试数据生成{args.gen_num}样本')
    selected_domains = Counter(selected_domains).most_common()
    selected_qualities = Counter(selected_qualities).most_common()
    print(f'[!] domain distribution:', selected_domains)
    print(f'[!] quality distribution:', selected_qualities)
    return dataset

    #for category, value in few_shot.items():
    #    for quality, samples in value.items():
    #        prompt_string = prompt.format(
    #            responsequality=quality,
    #            domain=category,
    #            generationnum=args.gen_num,
    #            reference=reference,
    #            domaindef=few_shot_detail[category]
    #        )
    #        dataset.append((prompt_string, category, quality))
    #print(f'[!] 合成了{len(dataset)}的测试数据')
    #return dataset


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
    for index in tqdm(range(0, len(dataset[cache_num:]), args.bsz)):
        samples_ = dataset[cache_num+index:cache_num+index+args.bsz]
        batch = []
        for prompt_string, category, quality, _ in samples_:
            batch.append([{'role': 'user', 'content': prompt_string}])
        responses = batch_chat(batch)
        assert len(batch) == len(responses)
        for j, (s, b, r) in enumerate(list(zip(samples_, batch, responses))):
            b.append({'role': 'assistant', 'content': r})
            file_name_suffix = f'_{s[1]}_{s[2]}_{s[3]}'
            with open(os.path.join(output_path, str(cache_num+index+j) + file_name_suffix + '.json'), 'w') as f:
                json.dump(b, f, ensure_ascii=False, indent=4)


def batch_chat_with_api(dataset, output_path):
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
    for index in tqdm(range(0, len(dataset[cache_num:]), args.bsz)):
        samples_ = dataset[cache_num+index:cache_num+index+args.bsz]
        batch = []
        for prompt_string, category, quality in samples_:
            batch.append([{'role': 'user', 'content': prompt_string}])
        responses = batch_chat(batch)
        assert len(batch) == len(responses)
        for j, (s, b, r) in enumerate(list(zip(samples_, batch, responses))):
            b.append({'role': 'assistant', 'content': r})
            file_name_suffix = f'_{s[1]}_{s[2]}'
            with open(os.path.join(output_path, str(cache_num+index+j) + file_name_suffix + '.json'), 'w') as f:
                json.dump(b, f, ensure_ascii=False, indent=4)


def batch_chat_with_api_meta_evaluation(dataset, output_path, prompt_temp):
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
    for index in tqdm(range(0, len(dataset[cache_num:]), args.bsz)):
        samples_ = dataset[cache_num+index:cache_num+index+args.bsz]
        # make the prompt_string
        prompt_strings = [prompt_temp.format(query=sample_['raw_data']['query'], response=sample_['raw_data']['response'], critique=sample_['raw_data']['critique'], predictioncritique=sample_['prediction']) for sample_ in samples_]

        batch = []
        for prompt_string in prompt_strings:
            batch.append([{'role': 'user', 'content': prompt_string}])
        responses = batch_chat(batch)
        assert len(batch) == len(responses)
        for j, (s, b, r) in enumerate(list(zip(samples_, batch, responses))):
            b.append({'role': 'assistant', 'content': r})
            file_name_suffix = f'_{s["category"]}_{s["quality"]}'
            with open(os.path.join(output_path, str(cache_num+index+j) + file_name_suffix + '.json'), 'w') as f:
                json.dump(b, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    prompt = open('prompts/data_generation_v2.md').read()
    few_shot = json.load(open('new_few_shot.json'))
    few_shot_detail = json.load(open('few_shot_detail_v2.json'))

    ####### one loop #######
    if args.mode == 'test_set_construction':
        ########## 1. generate test set  [test_set_construction]
        test_set = generate_test_data(few_shot)
        subfolder_name = f'test_set_gn_{args.test_query_num}_{args.gen_num}_fsn_{args.few_shot_num}'
        print('=' * 20)
        print(f'[!] save data into {subfolder_name}')
        print('=' * 20)
        if os.path.exists(args.root_path) is False:
            os.makedirs(args.root_path)
        if os.path.exists(os.path.join(args.root_path, f'iter_{args.iter_num}')) is False:
            os.makedirs(os.path.join(args.root_path, f'iter_{args.iter_num}'))
        if os.path.exists(os.path.join(args.root_path, f'iter_{args.iter_num}', subfolder_name)) is False:
            os.makedirs(os.path.join(args.root_path, f'iter_{args.iter_num}', subfolder_name))
        batch_chat_with_api(test_set, f'{args.root_path}/iter_{args.iter_num}/{subfolder_name}')
    elif args.mode == 'evaluate':
        save_path =  f'{args.root_path}/iter_{args.iter_num}/{args.model_prediction_name}.json'
        if os.path.exists(save_path) is True:
            print(f'[!] found the generated file:', save_path)
            exit()
        ########## 2. evaluate model performance on these test set
        model = OpenLLM(args.model_path, args.model_prompt, args.model_bsz)
        subfolder_name = f'test_set_gn_{args.test_query_num}_{args.gen_num}_fsn_{args.few_shot_num}'
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
    elif args.mode == 'meta_evaluate':
        prompt_template = open('prompts/meta_evaluation.md').read()
        save_path =  f'{args.root_path}/iter_{args.iter_num}/{args.model_prediction_name}.json'
        model_prediction = json.load(open(save_path))
        if os.path.exists(os.path.join(args.root_path, f'iter_{args.iter_num}', 'meta_evaluation')) is False:
            os.makedirs(os.path.join(args.root_path, f'iter_{args.iter_num}', 'meta_evaluation'))
        batch_chat_with_api_meta_evaluation(model_prediction, f'{args.root_path}/iter_{args.iter_num}/meta_evaluation', prompt_template)
    elif args.mode == 'train_set_construction':
        # quality error dis, domain error dis
        failure_dis = json.load(open(args.failure_dis_file))
        domain_dis, quality_dis = failure_dis['domain_dis'], failure_dis['quality_dis']
        train_set = generate_train_data(few_shot, domain_dis, quality_dis)
        subfolder_name = f'train_set_gn_{args.train_query_num}_{args.train_num_each}_fsn_{args.few_shot_num}_mode_{args.dis_mode}_rate_{args.mixture_rate}'
        batch_chat_with_api_train(train_set, f'{args.root_path}/iter_{args.iter_num}/{subfolder_name}')

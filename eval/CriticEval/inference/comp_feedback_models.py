from utils import *
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import transformers
#from vllm import LLM, SamplingParams
import torch
from transformers.generation import GenerationConfig
from transformers import pipeline, LlamaTokenizer, LlamaForCausalLM
import json
import os
import sys
import ipdb
import argparse


'''各种llm的推理脚本'''


def parser_args():
    parser = argparse.ArgumentParser(description='train parameters')
    parser.add_argument('--output_dir', type=str, default='outputs')
    parser.add_argument('--data_dir', type=str, default='../data/CriticBench')
    parser.add_argument('--split', type=str, default='test')
    parser.add_argument('--default', type=str, default='False')
    parser.add_argument('--model_name', type=str, default='internlm/internlm2-chat-7b')
    parser.add_argument('--reference', type=str, default='True')
    parser.add_argument('--task', type=str, default='True')
    parser.add_argument('--criteria', type=str, default='True')
    return parser.parse_args() 


if __name__ == "__main__":
    args = vars(parser_args())
    args['default'] = eval(args['default'])
    args['reference'] = eval(args['reference'])
    args['task'] = eval(args['task'])
    args['criteria'] = eval(args['criteria'])
    set_names = [
        'translate',
        'qa',
        'chat',
        'summary',
        'harmlessness',
        'math_cot',
        'math_pot',
        'code_exec',
        'code_not_exec'
    ]
    mode_name = 'comp_feedback'
    model = OpenLLM(args['model_name'])
    if os.path.exists(args['output_dir']) is False:
        os.makedirs(args['output_dir'])
    if os.path.exists(os.path.join(args['output_dir'], args['model_name'].replace('/', '_'))) is False:
        os.makedirs(os.path.join(args['output_dir'], args['model_name'].replace('/', '_')))
    folder_path = os.path.join(args['output_dir'], args['model_name'].replace('/', '_'))
    if os.path.exists(folder_path) is False:
        os.makedirs(folder_path)

    for set_name in tqdm(set_names):
        datasets = load_all_datasets(args['data_dir'], split=args['split'], mode_name=mode_name, set_name=set_name)
        for abbr, dataset in datasets.items():
            path = os.path.join(folder_path, abbr + ".json")
            if os.path.exists(path) is True:
                print('=' * 50)
                print(f'[!] skip existing file:', path)
                print('=' * 50)
                continue
            
            prompts = []
            for item in dataset['dev']:
                item['raw_data'] = json.loads(item['raw_data'])
                prompts.append(item)
                #ipdb.set_trace()

            #responses = model.batch_chat_basemodel(prompts, set_name=set_name)
            #responses = model.batch_chat_comp(prompts, set_name=set_name)
            responses = model.batch_chat_comp_reward_model(prompts, set_name=set_name)
            results = {}
            assert len(dataset['dev']) == len(responses)
            for item, response in zip(dataset['dev'], responses):
                results[str(len(results))] = {
                    'origin_prompt': item['question'],
                    'prediction': response
                }

            with open(path, 'w') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
            print('=' * 50)
            print(f'[!] save file into:', path)
            print('=' * 50)

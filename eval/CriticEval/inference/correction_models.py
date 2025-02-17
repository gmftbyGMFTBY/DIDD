from utils import *
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import transformers
from vllm import LLM, SamplingParams
import torch
from transformers.generation import GenerationConfig
from transformers import pipeline, LlamaTokenizer, LlamaForCausalLM
import json
import os
import sys
import ipdb
import argparse
from utils import *


'''各种llm的推理脚本'''


def parser_args():
    parser = argparse.ArgumentParser(description='train parameters')
    parser.add_argument('--output_dir', type=str, default='outputs')
    parser.add_argument('--data_dir', type=str, default='../data/CriticBench')
    parser.add_argument('--split', type=str, default='test')
    parser.add_argument('--model_name', type=str, default='internlm/internlm2-chat-7b')
    parser.add_argument('--inference_model_name', type=str, default='internlm/internlm2-chat-7b')
    return parser.parse_args() 


if __name__ == "__main__":
    args = vars(parser_args())
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
    mode_name = 'correction'
    if os.path.exists(args['output_dir']) is False:
        os.makedirs(args['output_dir'])
    if os.path.exists(os.path.join(args['output_dir'], args['model_name'].replace('/', '_'))) is False:
        os.makedirs(os.path.join(args['output_dir'], args['model_name'].replace('/', '_')))
    folder_path = os.path.join(args['output_dir'], args['model_name'].replace('/', '_'))
    
    model = OpenLLM(args['inference_model_name'])

    for set_name in tqdm(set_names):
        datasets = load_all_datasets(os.path.join(args['data_dir'], args['model_name'].replace('/', '_')), split=args['split'], mode_name=mode_name, set_name=set_name)
        for abbr, dataset in datasets.items():
            path = os.path.join(folder_path, abbr + ".json")
            if os.path.exists(path) is True:
                print(f'=' * 50)
                print(f'[!] skip existing file:', path)
                print(f'=' * 50)
                continue
            prompts = [item for item in dataset['dev']]
            # responses = model.batch_chat(prompts)
            responses = model.batch_chat_correction(prompts, set_name)
            results = {}
            assert len(dataset['dev']) == len(responses)
            for response, item in zip(responses, dataset['dev']):
                results[str(len(results))] = {
                    'origin_prompt': item['question'],
                    'prediction': response
                }
            with open(path, 'w') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)

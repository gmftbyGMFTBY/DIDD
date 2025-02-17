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


'''各种llm的推理脚本'''


def parser_args():
    parser = argparse.ArgumentParser(description='train parameters')
    parser.add_argument('--output_dir', type=str, default='outputs')
    parser.add_argument('--data_dir', type=str, default='../data/CriticBench')
    parser.add_argument('--split', type=str, default='test')
    parser.add_argument('--default', type=str, default='False')
    parser.add_argument('--model_name', type=str, default='internlm/internlm2-chat-7b')
    parser.add_argument('--version', type=int, default=1)
    return parser.parse_args() 


if __name__ == "__main__":
    args = vars(parser_args())
    args['default'] = eval(args['default'])
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
    if args['version'] == 1.0:
        mode_name = 'meta_feedback'
    else:
        mode_name = 'meta_feedback_no_ref'
    model = OpenLLM(args['model_name'])
    # for api model
    # model = OpenLLM(**{'model_name':'api_model', 'host': 'http://192.168.151.81', 'port': 2333})
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
            if args['default'] is True:
                responses = model.batch_chat_default(prompts)
            else:
                if model.model_name not in ['gpt-3.5-turbo', 'gpt-4-1106-preview', 'claude-instant-1']:
                    if model.model_name  == 'api_model':
                        responses = []
                        for prompt in tqdm(prompts):
                            history = [{'role': 'user', 'content': prompt['question']}]
                            response = model.chat_api(history)
                            responses.append(response)
                    else:
                        responses = model.batch_chat(prompts, set_name=set_name)
                else:
                    responses = model.batch_chat_close_source(prompts, batch_size=2)
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

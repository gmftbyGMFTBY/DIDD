from utils import *
from tqdm import tqdm
import json
import os
import ipdb
import argparse


'''各种llm的推理脚本'''


def parser_args():
    parser = argparse.ArgumentParser(description='train parameters')
    parser.add_argument('--output_dir', type=str, default='outputs')
    parser.add_argument('--model_name', type=str, default='internlm/internlm2-chat-7b')
    return parser.parse_args() 


if __name__ == "__main__":
    args = vars(parser_args())
    model = OpenLLM(args['model_name'])
    if os.path.exists(args['output_dir']) is False:
        os.makedirs(args['output_dir'])
    if os.path.exists(os.path.join(args['output_dir'], args['model_name'].replace('/', '_'))) is False:
        os.makedirs(os.path.join(args['output_dir'], args['model_name'].replace('/', '_')))
    folder_path = os.path.join(args['output_dir'], args['model_name'].replace('/', '_'))
    if os.path.exists(folder_path) is False:
        os.makedirs(folder_path)

    dataset = []
    with open('data/testdata_pairwise.jsonl') as f:
        for line in f.readlines():
            dataset.append(json.loads(line))
    print(f'[!] >>>>>')
    print('Counter:', len(dataset))
    print(f'[!] >>>>>')

    responses = model.batch_chat(dataset)
    #responses = model.batch_chat_reward_model(dataset)
    for response, data in zip(responses, dataset):
        data['evaluate'] = response 
    path = os.path.join(folder_path, f'result.json')
    with open(path, 'w') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)
    print('=' * 50)
    print(f'[!] save file into:', path)
    print('=' * 50)

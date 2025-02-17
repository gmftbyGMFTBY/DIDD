from utils import *
from copy import deepcopy
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
import re


'''parse生成的feedback结果整理成和../data/CriticBench一致的标注文件格式，以供correction任务使用
1. 读取原始的raw data数据
2. 读取生成的feedback data数据
3. 合并数据
4. 写数据
'''

def only_reserve_feedback(string):
    # remove response
    # assert '\n----------\n' in string
    if '\n----------\n' in string:
        strings = string.split('\n----------\n')
        assert len(strings) == 2
        string = strings[0]
    try:
        items = re.split('\n# Feedback\n', string)
        assert len(items) == 2
        #feedback = '\n# Evaluated Response with Symbols\n' + \
        #        strings[1] + '\n The evaluated responses are shown as above, and each sentence has been marked with a citation symbol, like [S1] or [S2]. These symbols will be used in the critiques below.\n\n' + \
        #        '\n# Feedback\n' + items[1]
        feedback = '\n# Feedback\n' + items[1]
        error = False
    except:
        error = True
        feedback = string
    return feedback, error

def parser_args():
    parser = argparse.ArgumentParser(description='train parameters')
    parser.add_argument('--output_dir', type=str, default='outputs')
    parser.add_argument('--data_dir', type=str, default='../data/CriticBench')
    parser.add_argument('--gen_feedback_data_dir', type=str, default='../output')
    parser.add_argument('--split', type=str, default='test')
    parser.add_argument('--model_name', type=str, default='internlm/internlm2-chat-7b')
    return parser.parse_args() 


def parse_root_path(path):
    '''correction_part数据不需要correction'''
    file_name = os.path.split(path)[-1]
    file_name = file_name.replace('math_cot', 'mathcot').replace('math_pot', 'mathpot').replace('code_exec', 'codeexec').replace('code_not_exec', 'codenotexec')
    items = file_name.replace('.json', '').split('_')
    split_name = items[0]
    set_name = items[1]
    if set_name == 'mathcot':
        set_name = 'math_cot'
    elif set_name == 'mathpot':
        set_name = 'math_pot'
    elif set_name == 'codeexec':
        set_name = 'code_exec'
    elif set_name == 'codenotexec':
        set_name = 'code_not_exec'
    assert items[2] == 'feedback'
    flag_name = items[3]
    if len(items) > 4:
        return None

    folder_path = f'{flag_name}_{split_name}_data'
    file_name = f'{set_name}_feedback_correction.json'
    folder_path = os.path.join(folder_path, file_name)
    return folder_path


def write_file(write_data, write_data_path):
    folder, file_name = os.path.split(write_data_path)
    if os.path.exists(folder) is False:
        os.makedirs(folder)
    with open(write_data_path, 'w') as f:
        json.dump(write_data, f, ensure_ascii=False, indent=4)


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
    mode_name = 'feedback'
    for set_name in tqdm(set_names):
        datasets = load_all_datasets(args['data_dir'], split=args['split'], mode_name=mode_name, set_name=set_name)
        errors = 0
        for abbr, dataset in datasets.items():

            if 'obj' in abbr:
                if 'math_cot' in abbr or 'math_pot' in abbr or 'code_exec' in abbr or 'code_not_exec' in abbr:
                    pass
                else:
                    continue

            # abbr是写入的feedback的数据
            # 读取对应的feedback data数据
            feedback_read_data_path = f'{args["gen_feedback_data_dir"]}/{args["model_name"].replace("/", "_")}/{abbr}.json'
            with open(feedback_read_data_path) as f:
                gen_feedback_data = json.load(f)
            # 读取raw data的路径信息
            raw_data_path = parse_root_path(feedback_read_data_path)
            if raw_data_path is None:
                continue
            read_raw_data_path = os.path.join(args['data_dir'], raw_data_path)
            with open(read_raw_data_path) as f:
                raw_feedback_data = json.load(f)
            # 整合生成的feedback数据
            assert len(raw_feedback_data) == len(gen_feedback_data)
            write_data = []
            for index in range(len(raw_feedback_data)):
                assert raw_feedback_data[index]['question'] in gen_feedback_data[str(index)]['origin_prompt']
                assert raw_feedback_data[index]['generation'] in gen_feedback_data[str(index)]['origin_prompt']
                write_data_ = deepcopy(raw_feedback_data[index])
                # TODO
                #write_data_['feedback'] = gen_feedback_data[str(index)]['prediction']
                ff, label = only_reserve_feedback(gen_feedback_data[str(index)]['prediction'])
                if label:
                    errors += 1
                write_data_['feedback'] = ff
                write_data.append(write_data_)
            # 替换raw_data的root_dir并写入
            write_data_path = os.path.join(f"{args['output_dir']}/{args['model_name'].replace('/', '_')}", raw_data_path)
            write_file(write_data, write_data_path)
        print(f'[!] error number for {set_name}: {errors}')


from evaluators import *
import time
import math
from tabulate import tabulate
from copy import deepcopy
import ipdb
import argparse
import os
import openai


def parser_args():
    parser = argparse.ArgumentParser(description='train parameters')
    parser.add_argument('--root_dir', type=str)
    parser.add_argument('--prediction_dir', type=str)
    parser.add_argument('--evaluation_dir', type=str)
    parser.add_argument('--split', type=str)
    parser.add_argument('--obj', type=str)
    parser.add_argument('--fast_mode', type=str, default='False')
    parser.add_argument('--batch_size', type=int)
    parser.add_argument('--ignore_models', nargs='+')
    parser.add_argument('--allow_models', nargs='+')
    return parser.parse_args() 


def evaluate_feedback_obj(
    root_dir, 
    prediction_dir, 
    ignore_models=[], 
    allow_models=[], 
    split='test', 
    # summary, math_cot, math_pot, code_exec, code_not_exec表现差，其他几个任务表现的很好
    # 正确样本的反思能力比ultracm和autoj要差(over critic)
    domains=[
        'translate', 
        'chat', 
        'qa', 
        'harmlessness', 
        'summary', 
        'math_cot', 
        'math_pot', 
        'code_exec', 
        'code_not_exec'
    ]
):
    tables_obj = []
    tables_obj_diff = {'low': [], 'med': [], 'high': [], 'super-high': []}
    for model in os.listdir(prediction_dir):

        # if 'auto-j' in model or 'autoj' in model or 'ultracm' in model:
        #     continue

        if ignore_models and model in ignore_models:
            print(f'[!] ignore model:', model)
            continue
        if allow_models and model not in allow_models:
            continue

        prediction_path, raw_data_path = [], []
        for domain in domains:
            raw_data_path.append(f'{root_dir}/obj_{split}_data/{domain}_feedback_correction.json')
            prediction_path.append(f'{prediction_dir}/{model}/{split}_{domain}_feedback_obj.json')
            if domain != 'code_exec':
                raw_data_path.append(f'{root_dir}/obj_{split}_data/correction_part/{domain}_feedback.json')
                prediction_path.append(f'{prediction_dir}/{model}/{split}_{domain}_feedback_obj_correction_part.json')

        evalutor = EvaluateScalarFeedback(
            prediction_path=prediction_path,
            raw_data_path=raw_data_path,
            split=split,
            flag='obj'
        )
        if len(evalutor.predictions) == 0:
            continue
        tables_obj.append([model])
        for q in tables_obj_diff:
            tables_obj_diff[q].append([model])

        #if 'autoj-13b' == model or 'autoj' in model:
        #    parse_score_func = autoj_parse_score_func
        #elif 'ultracm' == model or 'ultracm' in model or 'themis' in model or 'UltraCM' in model or 'promethues' in model:
        #    parse_score_func = extract_score 
        #elif 'tigerscore' == model or 'tigerscore' in model:
        #    parse_score_func = tigerscore_parse_score_func
        #else:
        #    parse_score_func = extract_score
        #     #parse_score_func = extract_decision
        parse_score_func = extract_score

        score, diff_resp_score = evalutor.evaluate(parse_score_func)
        tables_obj[-1].append(score)
        for q, v in diff_resp_score.items():
            tables_obj_diff[q][-1].append(v)
    # average for each domain
    tables_obj.append(['Average Domain'])
    for i in range(1, len(tables_obj[0])):
        aeds = [item[i] for item in tables_obj[:-1]]
        tables_obj[-1].append(round(np.nanmean(aeds), 2))
    table_obj = tabulate(tables_obj, headers=['models', 'Avg.'], tablefmt='simple')
    print('=' * 20, 'Feedback Objective', '=' * 20)
    print(table_obj)
    for q in tables_obj_diff:
        print('=' * 20, 'Feedback Objective Qualities', q, '=' * 20)
        table = tabulate(tables_obj_diff[q], headers=['models', 'Avg.'], tablefmt='simple')
        print(table)


def evaluate_feedback_sub(
    root_dir, 
    prediction_dir,
    evaluation_dir, 
    ignore_models=[], 
    allow_models=[], 
    split='test', 
    fast_mode=False, 
    batch_size=1,
    domains=[
        'translate', 
        'chat', 
        'qa', 
        'harmlessness', 
        'summary', 
        'math_cot', 
        'math_pot', 
        'code_exec', 
        'code_not_exec'
    ]
):
    # init the OpenAI API Key
    #openai.api_key = os.getenv("OPENAI_API_KEY")
    # evaluator_llm = OpenLLM('internlm2-20b-chat')
    evaluator_llm = None
    
    tables_sub = []
    tables_sub_diff = {'low': [], 'med': [], 'high': [], 'super-high': []}
    for model in os.listdir(prediction_dir):
        if os.path.isdir(os.path.join(prediction_dir, model)) is False:
            continue
        if ignore_models and model in ignore_models:
            print(f'[!] ignore model:', model)
            continue
        if allow_models and model not in allow_models:
            continue

        tables_sub.append([model])
        for q in tables_sub_diff:
            tables_sub_diff[q].append([model])

        raw_data_path, prediction_path, evaluation_path, domain_names = [], [], [], []
        for domain in domains:
            raw_data_path.append(f'{root_dir}/sub_{split}_data/{domain}_feedback_correction.json')
            prediction_path.append(f'{prediction_dir}/{model}/{split}_{domain}_feedback_sub.json')
            evaluation_path.append(f'{evaluation_dir}/{model}/{split}_{domain}_sub_feedback.jsonl')
            domain_names.append(domain)

            if domain != 'code_exec':
                raw_data_path.append(f'{root_dir}/sub_{split}_data/correction_part/{domain}_feedback.json')
                prediction_path.append(f'{prediction_dir}/{model}/{split}_{domain}_feedback_sub_correction_part.json')
                evaluation_path.append(f'{evaluation_dir}/{model}/{split}_{domain}_sub_feedback_correction_part.jsonl')
                domain_names.append(domain)
        # santiy check
        for path_a, path_b, path_c, domain_name in zip(raw_data_path, prediction_path, evaluation_path, domain_names):
            assert os.path.exists(path_a), f'{path_a} doesn"t exist'
            if os.path.exists(f'{prediction_dir}/{model}') is False:
                pass
                # assert os.path.exists(path_b), f'{path_b} doesn"t exist'
            if os.path.exists(f'{evaluation_dir}/{model}') is False:
                os.makedirs(f'{evaluation_dir}/{model}')
            assert domain_name in path_a and domain_name in path_b and domain_name in path_c
        
        evalutor = EvaluateNLFeedback(
            flag='sub',
            split=split,
            fast_mode=fast_mode,
            raw_data_path=raw_data_path,
            prediction_path=prediction_path,
            evaluation_path=evaluation_path,
            domain_names=domain_names,
            evaluator_llm=evaluator_llm)
        if evalutor.valid is False:
            continue
        # print('=' * 20, f'evaluate {model} on feedback task with {len(raw_data_path)} files', '=' * 20)
        scores, diff_resp_scores = evalutor.batch_evaluate(batch_size=batch_size)
        for domain in domains:
            tables_sub[-1].append(scores[domain])
            for q in ['low', 'med', 'high', 'super-high']:
                if q == 'super-high' and domain == 'code_exec':
                    value = math.nan
                else:
                    value = diff_resp_scores[domain][q]
                tables_sub_diff[q][-1].append(value)
        tables_sub[-1].append(round(np.nanmean(tables_sub[-1][1:]), 2))
        for q in ['low', 'med', 'high', 'super-high']:
            tables_sub_diff[q][-1].append(round(np.nanmean(tables_sub_diff[q][-1][1:]), 2))
    # average for each domain
    tables_sub.append(['Average Domain'])
    for i in range(1, len(tables_sub[0])):
        aeds = [item[i] for item in tables_sub[:-1]]
        tables_sub[-1].append(round(np.nanmean(aeds), 2))
    table_sub = tabulate(tables_sub, headers=['models'] + domains + ['Avg.'], tablefmt='simple')
    print('=' * 20, 'Feedback Subjective', '=' * 20)
    print(table_sub)
    for q in tables_sub_diff:
        print('=' * 20, 'Feedback Subjective Qualities', q, '=' * 20)
        table = tabulate(tables_sub_diff[q], headers=['models'] + domains + ['Avg.'], tablefmt='simple')
        print(table)

if __name__ == "__main__":
    args = vars(parser_args())
    if args['obj'] == 'True':
        evaluate_feedback_obj(
            args['root_dir'],
            args['prediction_dir'],
            ignore_models=args['ignore_models'],
            allow_models=args['allow_models'],
            split=args['split']
        )
    else:
        if os.path.exists(args['evaluation_dir']) is False:
            os.makedirs(args['evaluation_dir'])
        evaluate_feedback_sub(
            args['root_dir'],
            args['prediction_dir'],
            args['evaluation_dir'],
            ignore_models=args['ignore_models'],
            allow_models=args['allow_models'],
            split=args['split'],
            batch_size=args['batch_size'],
            fast_mode=eval(args['fast_mode'])
        )

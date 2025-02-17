import os
from .themis_utils import *
from criteria_for_qs import question_source_dict
import re
from .prompts_v2 import *
from .nips2024_prompts import *
from tqdm import tqdm
try:
    from tigerscore import TIGERScorer
except:
    pass
from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig, ChatTemplateConfig
import ipdb
import re
import json
import time
#from vllm import SamplingParams
from transformers import AutoTokenizer, AutoConfig
import openai
import tiktoken

import evaluate_configuration
from model_template import UltraCM, AutoJ


singlewise_prompt_template = open('singlewise_critique.md').read()


def prepare_prompt(item):
    conversation_input = f'[begin of conversation] user: {item["question"]} [end of conversation]'
    prompt = singlewise_prompt_template.format(conversation=conversation_input, response=item['generation'])
    return [{'role': 'user', 'content': prompt}]


def prepare_question_with_template(sample, question_template, task):
    question = sample["question"]
    if task == "generation":
        blank_list = re.findall("\{question}", question_template)
        context_for_blank = [question]
    elif task == "critique":
        response = sample["response"]
        dataset = sample["question_source"]
        if dataset == "HumanEval":
            blank_list = re.findall("\{solution}", question_template)
            context_for_blank = [response]
        else:
            blank_list = re.findall("\{question}|\{solution}", question_template)
            context_for_blank = [question, response]
    elif task == "correction":
        response = sample["response"]
        critique = sample["critique"]

        # replace the critique
        if '# Feedback' in critique:
            try:
                items = re.split('# Feedbacks\n', critique)
                try:
                    assert len(items) == 2
                except:
                    items = re.split('# Feedback\n', critique)
                    assert len(items) == 2
                critique = '# Feedbacks\n' + items[1]
            except:
                print(f'[!] MEET ERROR!!!')

        dataset = sample["question_source"]
        if dataset == "HumanEval":
            blank_list = re.findall("\{solution}|\{critique}", question_template)
            context_for_blank = [response, critique]
        else:
            blank_list = re.findall("\{question}|\{solution}|\{critique}", question_template)
            context_for_blank = [question, response, critique]
        pass
    assert len(blank_list) == len(context_for_blank)
    for b, c in zip(blank_list, context_for_blank):
        question_template = question_template.replace(b, c)
    return question_template

def set_prompt(model_path, task, max_gen_len,  dataset_with_prompt, model_from_api=False):
    if model_from_api:
        tokenizer = tiktoken.encoding_for_model(model_path)
        limit_length = evaluate_configuration.model_from_api_limit_length[model_path]
    else:
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
        config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
        limit_length = config.max_position_embeddings
    for sample in dataset_with_prompt:
        question = prepare_question_with_template(sample=sample,
                                                  question_template=sample["prompt_info_dict"]["question_template"],
                                                  task=task)
        instruction = sample["prompt_info_dict"]["instruction"]
        question_source = sample["question_source"]
        split_sep = evaluate_configuration.few_shot_split_sep_by_task[task][question_source]
        example_list = (sample["prompt_info_dict"]["examples"].split(split_sep))
        final_prompt = instruction + question
        model_template_len = 0
        for i in range(len(example_list)):
            examples = split_sep.join(example_list[:i+1])
            final_prompt = instruction + examples + question
            input_length = len(tokenizer.encode(final_prompt))
            if input_length > limit_length - max_gen_len - model_template_len:
                if split_sep == "\n---":
                    question = "\n---\n" + question
                final_prompt = instruction + split_sep.join(example_list[:i]) + question
                break
        final_prompt = final_prompt.strip()
        sample["final_prompt"] = final_prompt.strip()
    return dataset_with_prompt


def infer_hf(model, llm, dataset_with_prompt, out_dir, task, prompt_type):
    '''internlm2 and llama2 model'''
    max_gen_len = 1024
    tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)
    model_name = model.split("/")[-1]
    save_dir = os.path.join(out_dir, model_name, task)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    dataset_with_prompt = set_prompt(model_path=model, task=task, max_gen_len=max_gen_len,
                                     dataset_with_prompt=dataset_with_prompt, model_from_api=False)
    print("Number of samples: ", len(dataset_with_prompt))
    inputs = [sample["final_prompt"] for sample in dataset_with_prompt]

    outputs = []
    gen_config = GenerationConfig(temperature=0.0, max_new_tokens=4096)
    index = 0
    batch_size = 16
    pbar = tqdm(total=len(inputs))
    while index < len(inputs):
        msgs_ = [[{'role': 'user', 'content': input}] for input in inputs[index:index+batch_size]]
        responses = llm(msgs_, gen_config=gen_config)
        responses = [response.text for response in responses]
        index += batch_size
        outputs.extend(responses)
        pbar.update(len(msgs_)) 

    assert len(inputs) == len(outputs)
    result_list = [{"id":sample["id"], "final_prompt": sample['final_prompt'], f'{task}_result': output} for sample, output in zip(dataset_with_prompt, outputs)]

    save_path = os.path.join(save_dir, f"{prompt_type}_result_{time.strftime('%m_%d_%H_%M_%S', time.localtime(time.time()))}.jsonl")

    with open(save_path, "w", encoding="utf-8") as f:
        for sample in result_list:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
    return result_list


def set_critic_model_prompt(model, dataset):
    for sample in dataset:
        question = sample["question"]
        response = sample["response"]
        if "UltraCM-13b" in model:
            final_prompt = UltraCM.get_prompt(question=question, response=response)
            sample["final_prompt"] = final_prompt.strip()
        elif "autoj-13b" in model:
            final_prompt = AutoJ.get_prompt(question=question, response=response)
            sample["final_prompt"] = final_prompt.strip()
        elif 'TIGERScore' in model:
            sample["final_prompt"] = ('', question, response)
        elif 'Themis' in model:
            sample['final_prompt'] = ('', (question, response, sample['question_source']))
        else:
            sample["final_prompt"] = ('Please solve the question effectively!', question, response, sample['question_type'], sample['question_source'])
    return dataset


def infer_hf_critic_model(model, llm, dataset, out_dir, task):
    '''auto-j, ultracm, tigerscore'''
    _infer_hf_critic_model_v3(model, llm, dataset, out_dir, task)


def _infer_hf_critic_model_v3(model, llm, dataset, out_dir, task):
    '''internlm2 model with lmdeploy inference'''
    max_gen_len = 2048
    model_name = model.replace('/', '_')
    print("Number of samples: ", len(dataset))

    save_dir = os.path.join(out_dir, model_name, task)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
    dataset_with_prompt = set_critic_model_prompt(model, dataset)

    inputs = [sample["final_prompt"] for sample in dataset_with_prompt]
    batch_size = 32
    index = 0
    pbar = tqdm(total=len(inputs))
    outputs = []
    gen_config = GenerationConfig(temperature=0.0, max_new_tokens=2048)
    while index < len(inputs):
        msgs_ = inputs[index:index+batch_size]
        msgs_ = [prepare_prompt({'question': msg[1], 'generation': msg[2]}) for msg in msgs_]
        responses = llm(msgs_, gen_config=gen_config)
        responses = [response.text for response in responses]
        index += batch_size
        outputs.extend(responses)
        pbar.update(len(msgs_)) 

    result_list = [{"id":sample["id"], "final_prompt":sample["final_prompt"],
                    f'{task}_result': output} for sample, output in zip(dataset_with_prompt, outputs)]

    save_path = os.path.join(save_dir, f"result_{time.strftime('%m_%d_%H_%M_%S', time.localtime(time.time()))}.jsonl")

    with open(save_path, "w", encoding="utf-8") as f:
        for sample in result_list:
            f.write(json.dumps(sample, ensure_ascii=False) + "\n")
    return result_list

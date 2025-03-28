import json
from .themis_utils import *
from .llm import *
from .prompts_v2 import *
import re
from .nips2024_prompts import *
from tqdm import tqdm
from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig, ChatTemplateConfig
import torch
import torch
import pprint
import tiktoken
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModelForSequenceClassification
from transformers.generation import GenerationConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, AutoConfig, AutoModel, LlamaTokenizer, LlamaForCausalLM
from accelerate import init_empty_weights,infer_auto_device_map,load_checkpoint_in_model,dispatch_model, load_checkpoint_and_dispatch
from lmdeploy.serve.openai.api_client import APIClient
from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig
import ipdb
import sys
try:
    from util_func import *
except:
    pass
from multiprocessing import Pool
import random
import time

def prepare_prompt_comp_reward_model(item, instruction, mode, prompt, generation_name):
    if mode != 'code_exec':
        return [
            {'role': 'user', 'content': f'{instruction}\n{item["raw_data"]["question"]}'},
            {'role': 'assistant', 'content': item['raw_data'][generation_name]}
        ]
    else:
        return [
            {'role': 'user', 'content': f'{instruction}\n{item["raw_data"]["question"]}'},
            {'role': 'assistant', 'content': item['raw_data'][generation_name]}
        ]


def prepare_prompt_comp(item, instruction, mode, prompt):
    if mode != 'code_exec':
        conversation = f'[begin of conversation] user: {instruction} {item["raw_data"]["question"]} [end of conversation]'
        responsea, responseb = item['raw_data']['generation_a'], item['raw_data']['generation_b']
    else:
        conversation = f'[begin of conversation] user: {instruction} {item["raw_data"]["question"]} [end of conversation]'
        responsea = f'{item["raw_data"]["generation_a"]} # execution results on the unit tests of this code are:\n{item["raw_data"]["exec_rest_a"]}'
        responseb = f'{item["raw_data"]["generation_b"]} # execution results on the unit tests of this code are:\n{item["raw_data"]["exec_rest_b"]}'
    ipt = prompt.format(conversation=conversation, responsea=responsea, responseb=responseb)
    return [{'role': 'user', 'content': ipt}]


def prepare_prompt_reward_model(item, instruction, mode, prompt):
    if mode != 'code_exec':
        return [
            {'role': 'user', 'content': f'{instruction}\n{item["raw_data"]["question"]}'},
            {'role': 'assistant', 'content': item['raw_data']['generation']}
        ]
    else:
        return [
            {'role': 'user', 'content': f'{instruction}\n{item["raw_data"]["question"]}'},
            {'role': 'assistant', 'content': f'{item["raw_data"]["generation"]} # execution results on the unit tests of this code are:\n{item["raw_data"]["exec_rest"]}'}
        ]


def prepare_prompt(item, instruction, mode, prompt):
    if mode != 'code_exec':
        conversation = f'[begin of conversation] user: {instruction} {item["raw_data"]["question"]} [end of conversation]'
        response = item['raw_data']['generation']
    else:
        conversation = f'[begin of conversation] user: {instruction} {item["raw_data"]["question"]} [end of conversation]'
        response = f'{item["raw_data"]["generation"]} # execution results on the unit tests of this code are:\n{item["raw_data"]["exec_rest"]}'
    ipt = prompt.format(conversation=conversation, response=response)
    return [{'role': 'user', 'content': ipt}]


def prepare_prompt_basemodel(item, instruction, mode):
    pass


class OpenLLM:

    def __init__(self, model_name='api_model'):
        self.model_name = model_name
        backend_config = PytorchEngineConfig(session_len=32768, tp=1)
        self.gen_config = GenerationConfig(temperature=0.0, max_new_tokens=2048)
        if 'Llama-3' in model_name or 'llama' in model_name:
            self.pipe = pipeline(model_name, backend_config=backend_config, chat_template_config=ChatTemplateConfig(model_name="llama"))
        elif 'Qwen' in model_name:
            self.pipe = pipeline(model_name, backend_config=backend_config, chat_template_config=ChatTemplateConfig(model_name="qwen"))
        elif model_name == 'internlm2-20b-reward':
            self.model = AutoModel.from_pretrained(
                "/home/lt/reward_models/internlm/internlm2-20b-reward",
                torch_dtype=torch.float16, 
                device_map='auto',
                trust_remote_code=True,
            )
            self.tokenizer = AutoTokenizer.from_pretrained("/home/lt/reward_models/internlm/internlm2-20b-reward", trust_remote_code=True)
        elif model_name == 'skywork-reward-8b':
            self.device = "cuda:0"
            model_name = '/home/lt/reward_models/Skywork-Reward-Llama-3.1-8B'
            self.model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                torch_dtype=torch.bfloat16,
                device_map=self.device,
                num_labels=1,
            )
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        else:
            self.pipe = pipeline(model_name, backend_config=backend_config, chat_template_config=ChatTemplateConfig(model_name="internlm2"))
        self.prompt = open('utils/singlewise_critique.md').read()
        #self.prompt = open('utils/pairwise_critique.md').read()
    
    @torch.no_grad()
    def batch_chat_reward_model(self, msgs, max_new_tokens=2048, set_name=''):
        index, batch_size = 0, 4
        pbar = tqdm(total=len(msgs))
        outputs = []
        instruction = instruction_prompts[set_name]
        while index < len(msgs):
            msgs_ = [
                prepare_prompt_reward_model(msg, instruction, set_name, self.prompt) for msg in msgs[index:index+batch_size]
            ]
            if self.model_name == 'internlm2-20b-reward':
                responses = self.model.get_scores(self.tokenizer, msgs_)
            else:
                responses = []
                for msgs_one in msgs_:
                    conv1_formatted = self.tokenizer.apply_chat_template(msgs_one, tokenize=False)
                    conv1_tokenized = self.tokenizer(conv1_formatted, return_tensors="pt").to(self.device)
                    with torch.no_grad():
                        score = self.model(**conv1_tokenized).logits[0][0].item()
                    responses.append(score)
            if type(responses) == float:
                responses = [responses]
            responses = [str(response) for response in responses]
            index += batch_size
            outputs.extend(responses)
            pbar.update(len(msgs_))
        return outputs

    @torch.no_grad()
    def batch_chat(self, msgs, max_new_tokens=2048, set_name=''):
        index, batch_size = 0, 32
        pbar = tqdm(total=len(msgs))
        outputs = []
        instruction = instruction_prompts[set_name]
        while index < len(msgs):
            msgs_ = [
                prepare_prompt(msg, instruction, set_name, self.prompt) for msg in msgs[index:index+batch_size]
            ]
            responses = self.pipe(msgs_, gen_config=self.gen_config)
            responses = [response.text for response in responses]
            index += batch_size
            outputs.extend(responses)
            pbar.update(len(msgs_))
        return outputs

    @torch.no_grad()
    def batch_chat_basemodel(self, msgs, max_new_tokens=2048, set_name=''):
        index, batch_size = 0, 32
        pbar = tqdm(total=len(msgs))
        outputs = []
        instruction = instruction_prompts[set_name]
        while index < len(msgs):
            #msgs_ = [[{'role': 'user', 'content': msg['question']}] for msg in msgs[index:index+batch_size]]
            msgs_ = [prepare_prompt_comp(msg, instruction, set_name, self.prompt) for msg in msgs[index:index+batch_size]]
            #msgs_ = [prepare_prompt(msg, instruction, set_name, self.prompt) for msg in msgs[index:index+batch_size]]
            responses = self.pipe(msgs_, gen_config=self.gen_config)
            responses = [response.text for response in responses]
            index += batch_size
            outputs.extend(responses)
            pbar.update(len(msgs_))
        return outputs

    @torch.no_grad()
    def batch_chat_comp(self, msgs, max_new_tokens=2048, set_name=''):
        index, batch_size = 0, 32
        pbar = tqdm(total=len(msgs))
        outputs = []
        instruction = instruction_prompts[set_name]
        while index < len(msgs):
            msgs_ = [
                prepare_prompt_comp(msg, instruction, set_name, self.prompt) for msg in msgs[index:index+batch_size]
            ]
            responses = self.pipe(msgs_, gen_config=self.gen_config)
            responses = [response.text for response in responses]
            index += batch_size
            outputs.extend(responses)
            pbar.update(len(msgs_))
        return outputs

    @torch.no_grad()
    def batch_chat_comp_reward_model(self, msgs, max_new_tokens=2048, set_name=''):
        outputs_ = []
        instruction = instruction_prompts[set_name]
        generation_names = ['generation_a', 'generation_b']
        for generation_name in generation_names:
            outputs = []
            index, batch_size = 0, 4
            pbar = tqdm(total=len(msgs))
            while index < len(msgs):
                msgs_ = [
                    prepare_prompt_comp_reward_model(msg, instruction, set_name, self.prompt, generation_name) for msg in msgs[index:index+batch_size]
                ]
                if self.model_name == 'internlm2-20b-reward':
                    responses = self.model.get_scores(self.tokenizer, msgs_)
                else:
                    responses = []
                    for msgs_one in msgs_:
                        conv1_formatted = self.tokenizer.apply_chat_template(msgs_one, tokenize=False)
                        conv1_tokenized = self.tokenizer(conv1_formatted, return_tensors="pt").to(self.device)
                        with torch.no_grad():
                            score = self.model(**conv1_tokenized).logits[0][0].item()
                        responses.append(score)
                if type(responses) == float:
                    responses = [responses]
                #responses = [str(response) for response in responses]
                index += batch_size
                outputs.extend(responses)
                pbar.update(len(msgs_))
            outputs_.append(outputs)

        rests = []
        for a, b in zip(outputs_[0], outputs_[1]):
            if a > b:
                rests.append('Label: A')
            else:
                rests.append('Label: B')
        return rests 



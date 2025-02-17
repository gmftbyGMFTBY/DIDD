import json
import re
from tqdm import tqdm
from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig
import torch
import torch
import pprint
import tiktoken
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, AutoConfig, AutoModel
from lmdeploy.serve.openai.api_client import APIClient
from lmdeploy import pipeline, GenerationConfig, PytorchEngineConfig
import ipdb
import sys
from multiprocessing import Pool
import random
import time

class OpenLLM:

    def __init__(self, model_name='internlm2-20b-chat', api_host='http://172.31.30.206', api_port=2333):
        self.model_name = model_name
        if model_name in ['internlm2-20b-chat']:
            self.model_name_ = model_name
            path = '/cpfs01/shared/public/public_hdd/llmeval/model_weights/hf_hub/models--internlm--internlm2-chat-20b/snapshots/3f710f76f56f8c40dc5dd800dbe66f3341cb2c87'
            backend_config = PytorchEngineConfig(
                session_len=32768, 
                model_name='internlm2', 
                tp=1
            )
            self.gen_config = GenerationConfig(temperature=0.0, max_new_tokens=2048)
            self.pipe = pipeline(path, backend_config=backend_config)
            self.model_name_ = 'internlm2-20b-chat'
        elif model_name == 'api_model':
            path = f'{api_host}:{api_port}'
            self.api_client = APIClient(path)
            self.model_name_ = self.api_client.available_models[0]
        else:
            raise Exception(f'[!] Unknow model', model_name)

    @torch.no_grad()
    def batch_chat(self, payloads, temp=0.0):
        try:
            msgs = [payload['messages'] for payload in payloads]
            responses = self.pipe(msgs, gen_config=self.gen_config)
            responses = [response.text for response in responses]
            return responses
        except Exception as error:
            print(f'[!] request process WRONG for {self.model_name_}')
            sys.stdout.flush()
            return None

    def chat_api(self, history, temp=0.0):
        n = 0
        responses = []
        try:
            for his in history:
                for item in self.api_client.chat_completions_v1(
                    model=self.model_name_,
                    messages=his['messages'],
                    temperature=0.0,
                ):
                    if type(item) == str:
                        response = None
                    else:    
                        response = item['choices'][0]['message']['content']
                    responses.append(response)
                print(f'[!] request process SUCCESSFULLE for {self.model_name_}')
                sys.stdout.flush()
            return responses
        except Exception as error:
            print(f'[!] request process WRONG for {self.model_name_}:', error)
            sys.stdout.flush()
            return None


if __name__ == "__main__":
    model = OpenLLM(**{
        'model_name': 'api_model',
        'api_host': 'http://172.31.30.206',
        'api_port': 2333
    })
    response=model.chat_api([
        {
            'model': 'qwen',
            'messages': [
                {
                    'role': 'user',
                    'content': 'who are you?'
                }    
            ]
        },
    ])
    print(response)

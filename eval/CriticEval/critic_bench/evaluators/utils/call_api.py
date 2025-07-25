import json
import httpcore
import traceback
import random
import sys
from multiprocessing import Pool
import copy
import subprocess
import signal
import tempfile as tfile
import requests
import ipdb
import pprint
import time
import openai
from openai import OpenAI
from tqdm import tqdm
import subprocess
import os
from lagent.llms import GPTAPI


def _prepare_input(payload, temp, max_tokens, llm_name):
    if llm_name in ['gpt-3.5-turbo']:
        input_data = {
            'model': 'gpt-3.5-turbo',
            'messages': payload['messages'],
            'temperature': temp,
            'max_tokens': max_tokens
        }
    elif llm_name in ['gpt-4', 'gpt-4-1106-preview', 'gpt-4o']:
        input_data = {
            # 'model': 'gpt-4-1106-preview',
            'model': llm_name,
            'messages': payload['messages'],
            'temperature': temp,
            'max_tokens': max_tokens
        }
    else:
        raise Exception('[!] Unknow model name: {llm_name}')
    return input_data


def _chat_one_session_personal(payload, sleep_time, retry_num, temp, max_tokens, llm_name, index):

    def generate_single(
        client,
        prompt: str,
        model: str = 'gpt-4-1106-preview',
        **kwargs
    ) -> dict:
        success = False
        completion = None
        while not success:
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                success = True
                print(f'[!] one try success')
                rest = completion.choices[0].message.content
            except Exception as e:
                print(f'[!] one try failed', e)
                time.sleep(1)
                sys.stdout.flush()
                success = True
                rest = 'Score: None'

        return {
            "generation": rest,
            **kwargs
        }

    time_acc = 0
    base_url = 'https://api.ai-gaochao.cn/v1'
    api_key = 'sk-oI6T9QRH8uD1Yio64eFf81570f094f04A98cC7Eb7b0cB216'
    client = OpenAI(api_key=api_key, base_url=base_url)
    input_data = _prepare_input(payload, temp, max_tokens, llm_name)
    data = generate_single(client, input_data['messages'][0]['content'])
    response = data['generation']
    return response, index


def batch_chat(payloads, sleep_time=20, retry_num=5, temp=0.5, max_tokens=4096, model_name='gpt-4-1106-preview', debug=False):
    pool = Pool(processes=32)
    result_list = []
    for index, payload in enumerate(payloads):
        result_list.append(pool.apply_async(_chat_one_session_personal, (payload, sleep_time, retry_num, temp, max_tokens, model_name, index)))
    pool.close()
    pool.join()
    values = [rest.get() for rest in result_list]
    sorted_values = sorted(values, key=lambda x:x[-1])
    sorted_values = [i[0] for i in sorted_values]
    return sorted_values

if __name__ == "__main__":
    llm_name = 'gpt-4o'
    response = batch_chat([
            {
                'model': llm_name,
                'messages': [
                    {
                        'role': 'user',
                        'content': '你是谁'
                    }    
                ]
            },
        ],
        temp=0,
        model_name=llm_name,
    )
    print(response)

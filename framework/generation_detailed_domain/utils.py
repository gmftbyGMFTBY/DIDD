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


def _chat_one_session_personal(payload, sleep_time, retry_num, temp, max_tokens, llm_name, index):

    def generate_single(
        client,
        messages: list,
        model: str = 'gpt-4o',
        **kwargs
    ) -> dict:
        success = False
        completion = None
        while not success:
            try:
                completion = client.chat.completions.create(
                    model=model,
                    messages=messages,
                )
                success = True
                print(f'[!] one try success')
                rest = completion.choices[0].message.content
            except Exception as error:
                print(f'[!] one try failed:', error)
                time.sleep(1)
                sys.stdout.flush()
                success = True
                rest = None

        return {
            "generation": rest,
            **kwargs
        }

    time_acc = 0
    base_url = 'https://api.ai-gaochao.cn/v1'
    api_key = 'sk-e6Inw8EfZoi7sOE4A6De1d392f5e43Bd9299843d9333Ee49'
    client = OpenAI(api_key=api_key, base_url=base_url)
    data = generate_single(client, payload, llm_name)
    response = data['generation']
    return response, index


def batch_chat(payloads, sleep_time=20, retry_num=5, temp=0.8, max_tokens=4096, model_name='gpt-4o', debug=False):
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
            [
                {
                    'role': 'user',
                    'content': 'the history of china'
                }
            ]
        ],
        temp=0,
        model_name=llm_name,
    )
    print(response)

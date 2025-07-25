import json
import httpcore
import traceback
import random
import sys
from multiprocessing import Pool
# from latex2sympy2 import latex2sympy, latex2latex
import copy
import subprocess
# from pyext import RuntimeModule
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
    elif llm_name in ['claude-instant-1', 'claude-2']:
        input_data = {
            'model': llm_name,
            'prompt': payload['messages'][-1]['content'],
            'max_tokens': max_tokens,
            'temperature': temp
        }
    else:
        raise Exception('[!] Unknow model name: {llm_name}')
    return input_data


def _chat_one_session_personal(payload, sleep_time, retry_num, temp, max_tokens, llm_name, index):

    def generate_single(
        client,
        prompt: str,
        model: str = 'gpt-4o',
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
                    ],
                    temperature=0.0
                )
                success = True
                print(f'[!] one try success')
                rest = completion.choices[0].message.content
            #except httpcore.RemoteProtocolError or httpcore.ConnectTimeout:
            except Exception as error:
                print(f'[!] one try failed:', error)
                time.sleep(1)
                sys.stdout.flush()
                success = True
                rest = 'Score: None'

        return {
            #"generation": completion.choices[0].message.content,
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


def _chat_one_session(payload, sleep_time, retry_num, temp, max_tokens, llm_name, index):
    time_acc = 0
    if llm_name in ['gpt-4', 'gpt-4-1106-preview', 'gpt-3.5-turbo']:
        url = "http://ecs.sv.us.alles-apin.openxlab.org.cn/v1/openai/v2/text/chat"
        headers = {
            "content-type": "application/json",
            "alles-apin-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwidXNlcm5hbWUiOiJsYW50aWFuIiwiYXBwbHlfYXQiOjE2OTAxOTEwNTQxMjYsImV4cCI6MTg3MTYzMTA1NH0.XoYqnBY7bmzGNVSEmhPcHKWByjmslsZ2tvV9mceuJaw"
        }
    elif llm_name in ['claude-instant-1', 'claude-2']:
        url = "https://openxlab.org.cn/gw/alles-apin-hub/v1/claude/v1/text/chat"
        headers = {
            "content-type": "application/json",
            "alles-apin-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwidXNlcm5hbWUiOiJsYW50aWFuIiwiYXBwbHlfYXQiOjE2OTAxOTEwNTQxMjYsImV4cCI6MTg3MTYzMTA1NH0.XoYqnBY7bmzGNVSEmhPcHKWByjmslsZ2tvV9mceuJaw"
        }
    for _ in range(retry_num):
        if llm_name in ['gpt-4', 'gpt-4-1106-preview']:
            input_data = _prepare_input(payload, temp, max_tokens, llm_name)
            try:
                data = requests.post(url, headers=headers, data=json.dumps(input_data), timeout=200)
                response = data.json()['data']['choices'][0]['message']['content']
                prompt_tokens = data.json()['data']['usage']['prompt_tokens']
                completion_tokens = data.json()['data']['usage']['completion_tokens']
                sys.stdout.flush()
            except requests.exceptions.Timeout as errt:
                print(f'Exceed timeout error for {llm_name}:', errt)
                continue
            except Exception as error:
                print(f'[!] meet strange error:', error)
                print(data.text)
                sys.stdout.flush()
                time.sleep(5)
                continue

            if 'Rate limit reached for' in response:
                print(f'[!] You achieve the rate limit for {llm_name}, please sleep for 15 seconds')
                sys.stdout.flush()
                time.sleep(5)
            elif 'Error code' in response:
                print(f'[!] meet the error code for {llm_name}:', response)
                sys.stdout.flush()
                time.sleep(5)
            elif 'Bad gateway' in response:
                print(f'[!] Bad gateway occur, please sleep for 15 seconds for {llm_name}')
                sys.stdout.flush()
                time.sleep(5)
            elif response.startswith('\n<html><head>\n<meta type=\"copyright\" content=\"Copyright (C) 1996-2020 '):
                print(f'[!] GPT-4 turbo face the error, sleep 15 seconds')
                sys.stdout.flush()
                time.sleep(5)
            elif 'HTTPSConnectionPool' in response:
                print(f'[!] generation contains the HTTPS error in gpt-4 response')
                sys.stdout.flush()
                time.sleep(5)
            elif 'You exceeded your current quota' in response:
                print(f'[!] You exceeded your current quota for {llm_name}, please sleep for 15 seconds')
                sys.stdout.flush()
                time.sleep(5)
            elif len(response) == 0:
                print(f'[!] find no response from the API for {llm_name}')
                sys.stdout.flush()
                time.sleep(5)
            elif 'The server had an error while processing your request' in response:
                print(f'[!] The server had an error while processing your request for {llm_name}')
                sys.stdout.flush()
                time.sleep(5)
            elif 'Request timed out' in response:
                print(f'[!] meet request time out error for gpt-4, sleep 15 seconds')
                sys.stdout.flush()
                time.sleep(5)
            elif 'Alles-APIN' in response:
                print(f'[!] meet the APIN error for {llm_name}: {response}')
                sys.stdout.flush()
                time.sleep(5)
            else:
                print(f'[!] request process successfully for {llm_name}')
                sys.stdout.flush()
                return response, prompt_tokens, completion_tokens, index
        elif llm_name in ['gpt-3.5-turbo']:
            try:
                input_data = _prepare_input(payload, temp, max_tokens, llm_name)
                data = requests.post(url, headers=headers, data=json.dumps(input_data), timeout=200)
                response = data.json()['data']['choices'][0]['message']['content']
                prompt_tokens = data.json()['data']['usage']['prompt_tokens']
                completion_tokens = data.json()['data']['usage']['completion_tokens']
            except requests.exceptions.Timeout as errt:
                print('Exceed timeout error for {llm_name}:', errt)
                sys.stdout.flush()
                continue
            except Exception as error:
                print(f'[!] meet strange error:', error, data.json())
                sys.stdout.flush()
                # time.sleep(15)
                continue
            if 'Rate limit reached for' in response:
                print(f'[!] You achieve the rate limit, please sleep for 15 seconds for {llm_name}')
                sys.stdout.flush()
                time.sleep(5)
            elif 'HTTPSConnectionPool' in response:
                print(f'[!] generation contains the HTTPS error in gpt-4 response for {llm_name}')
                sys.stdout.flush()
                time.sleep(5)
            elif 'You exceeded your current quota' in response:
                print(f'[!] You exceeded your current quota, please sleep for 15 seconds for {llm_name}')
                sys.stdout.flush()
                time.sleep(5)
            elif len(response) == 0:
                print(f'[!] find no response from the API for {llm_name}')
                sys.stdout.flush()
                time.sleep(5)
            elif 'The server had an error while processing your request' in response:
                print(f'[!] The server had an error while processing your request for {llm_name}')
                sys.stdout.flush()
                return response, 0, 0, index
            elif 'Request timed out' in response:
                print(f'[!] meet request time out error for {llm_name}')
                sys.stdout.flush()
                # time.sleep(15)
            elif 'APIN' in response:
                print('meet APIN error for {llm_name}:', response)
                sys.stdout.flush()
                # time.sleep(15)
            elif 'Your account is not active' in response:
                print('Your account is not active for {llm_name}:', response)
                sys.stdout.flush()
                time.sleep(5)
            else:
                print(f'[!] run successfully for {llm_name}')
                sys.stdout.flush()
                return response, prompt_tokens, completion_tokens, index
        elif llm_name in ['claude-instant-1', 'claude-2']:
            try:
                input_data = _prepare_input(payload, temp, max_tokens, llm_name)
                data = requests.request('POST', url, headers=headers, data=json.dumps(input_data), timeout=200)
                response = json.loads(data.text)
                response = response['data']['completion']
                print(f'[!] request process successfully for {llm_name}')
                sys.stdout.flush()
                return response, 0, 0, index
            except requests.exceptions.Timeout as errt:
                print('Exceed timeout error for {llm_name}:', errt)
                sys.stdout.flush()
                time.sleep(5)
                continue
            except Exception as e:
                print(f'[!] Error for Claude:',  e)
                sys.stdout.flush()
                # if 'This request is blocked by Alles-APIN due to request rate limited' in data.text:
                #     print(f'[!] Claude meet the error:', 'This request is blocked by Alles-APIN due to request rate limite')
                #     sys.stdout.flush()
                time.sleep(5)
        time_acc += 5
    return None, 0, 0, index


def batch_chat(payloads, sleep_time=20, retry_num=5, temp=0.5, max_tokens=4096, model_name='gpt-4o', debug=False):
    if debug is True:
        for index, payload in enumerate(payloads):
            _chat_one_session_personal(payload, sleep_time, retry_num, temp, max_tokens, model_name, index)
    else:
        pool = Pool(processes=32)
        result_list = []
        for index, payload in enumerate(payloads):
            result_list.append(pool.apply_async(_chat_one_session_personal, (payload, sleep_time, retry_num, temp, max_tokens, model_name, index)))
        pool.close()
        pool.join()
        values = [rest.get() for rest in result_list]
        sorted_values = sorted(values, key=lambda x:x[-1])
        # sorted_values = [(i[0], i[1], i[2], i[3]) for i in sorted_values]
        sorted_values = [i[0] for i in sorted_values]
        return sorted_values

if __name__ == "__main__":
    llm_name = 'gpt-4o'
    #response = batch_chat_lagent_gptapi([
    response = batch_chat([
            {
                'model': llm_name,
                'messages': [
                    {
                        'role': 'user',
                        'content': 'mysql数据库如何插入数据的时候如何强制使用之前删除留下的剩余空间呢'
                    }    
                ]
            },
        ],
        temp=0,
        model_name=llm_name,
        debug=False
    )
    print(response)

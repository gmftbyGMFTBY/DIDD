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

try:
    lagent_gptapi = GPTAPI(
            model_type='gpt-4-1106-preview',
            #key='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',
        #key='sk-proj-sX50HQlcH9vbVFnjjoRiT3BlbkFJQeanIzaLIPRyMkXB1H5x',
        #key='sk-proj-uBpvprpgwoQ18AlfLSthT3BlbkFJOMu3C3V5JTfn5arc08Fb',
        key='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',
            query_per_second=50,
            max_new_tokens=4096,
            proxies=dict(
                    http=
                    'http://lantian:5trslplFamkoYwSb6Lk8TpwwpU2Tm1TWZDxf48k1OxzZsVAKo41GBgorgHa@closeai-proxy.pjlab.org.cn:23128',
                    https=
                    'http://lantian:5trslplFamkoYwSb6Lk8TpwwpU2Tm1TWZDxf48k1OxzZsVAKo41GBgorgHa@closeai-proxy.pjlab.org.cn:23128',
            ),
            retry=1
    ) 
except:
    pass


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
    api_key = 'sk-zhxjlLUVUsQokvKCF1211eB0196e48A3835586Cd7930C706'
    #base_url = 'https://api.shubiaobiao.com/v1'
    #api_key = 'sk-JvzfVevVfv22NURMvUPgJZox3PSIFq3gD6nNOW5Od7TvCuBR'
    client = OpenAI(api_key=api_key, base_url=base_url)
    input_data = _prepare_input(payload, temp, max_tokens, llm_name)
    data = generate_single(client, input_data['messages'][0]['content'])
    response = data['generation']
    return response, index


def _chat_one_session_openai(payload, sleep_time, retry_num, temp, max_tokens, llm_name, index):
    time_acc = 0
    if llm_name in ['gpt-4', 'gpt-4-1106-preview', 'gpt-3.5-turbo', 'gpt-4o']:
        # client = OpenAI(api_key='sk-proj-rNM7oZjf02KsfDNsKK8ZT3BlbkFJOITYZFVIrbEb2924LdGI')
        #client = OpenAI(api_key='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')
        #client = OpenAI(api_key='sk-proj-iLgkTTeWGUIhtSPkOFJQT3BlbkFJZ0ThetEqIYawzfa9k0eD')
        #client = OpenAI(api_key='sk-proj-sX50HQlcH9vbVFnjjoRiT3BlbkFJQeanIzaLIPRyMkXB1H5x')
        client = OpenAI(api_key='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')
    elif llm_name in ['claude-instant-1', 'claude-2']:
        url = "https://openxlab.org.cn/gw/alles-apin-hub/v1/claude/v1/text/chat"
        headers = {
            "content-type": "application/json",
            "alles-apin-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwidXNlcm5hbWUiOiJsYW50aWFuIiwiYXBwbHlfYXQiOjE2OTAxOTEwNTQxMjYsImV4cCI6MTg3MTYzMTA1NH0.XoYqnBY7bmzGNVSEmhPcHKWByjmslsZ2tvV9mceuJaw"
        }
    for retry_i in range(retry_num):
        if llm_name in ['gpt-4', 'gpt-4-1106-preview', 'gpt-4o', 'gpt-3.5-turbo']:
            input_data = _prepare_input(payload, temp, max_tokens, llm_name)
            try:
                # print(os.getenv('http_proxy'))
                # print(os.getenv('https_proxy'))
                # print(os.getenv('HTTP_PROXY'))
                # print(os.getenv('HTTPS_PROXY'))

                completion = client.chat.completions.create(
                    model=llm_name,
                    messages=input_data['messages']
                )
                response = completion.choices[0].message.content
                prompt_tokens = completion.usage.prompt_tokens
                completion_tokens = completion.usage.completion_tokens
            except openai.APIError as e:
                #Handle API error here, e.g. retry or log
                #t = 10 + 20 * random.random()
                t = 10
                print(f"OpenAI API returned an API Error, sleep {t} seconds", e)
                time.sleep(t)
                response = ''
                #traceback.print_exc()
            except openai.APIConnectionError as e:
                #Handle connection error here
                print(f"Failed to connect to OpenAI API: {e}")
                response = ''
            except openai.RateLimitError as e:
                #Handle rate limit error (we recommend using exponential backoff)
                #t = 10 + 20 * random.random()
                t = 10
                print(f"OpenAI API request exceeded rate limit, sleep {t} seconds")
                time.sleep(t)
                response = ''
            except Exception as error:
                print(error)
                response = ''
            sys.stdout.flush()

            if len(response) == 0:
                print(f'[!] Error find no response from the API for {llm_name}')
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
            else:
                print(f'[!] request process successfully for {llm_name}')
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
                # try:
                #     print(f'Exceed timeout error for {llm_name}:', errt, data.text)
                # except:
                print(f'Exceed timeout error for {llm_name}:', errt)

                # print('Exceed timeout error for {llm_name}:', errt)
                sys.stdout.flush()
                time.sleep(5)
                continue
            except Exception as e:
                try:
                    # print(f'[!] Error for Claude:',  e, data.text)
                    print(f'[!] Error for Claude:',  e)
                    sys.stdout.flush()
                    if 'This request is blocked by Alles-APIN due to request rate limited' in data.text:
                        print(f'[!] Claude meet the error:', 'This request is blocked by Alles-APIN due to request rate limite')
                        sys.stdout.flush()
                except:
                    print(f'[!] Error for Claude:',  e)
                time.sleep(5)
        time_acc += 5
        print(f'>>> retry time >>>', retry_i)
    return None, 0, 0, index




def _chat_one_session_azure(payload, sleep_time, retry_num, temp, max_tokens, llm_name, index):
    time_acc = 0
    if llm_name in ['gpt-4', 'gpt-4-1106-preview', 'gpt-3.5-turbo', 'gpt-4o']:
        url = "https://group-ck.openai.azure.com/openai/deployments/CK1/chat/completions?api-version=2024-02-01"
        headers = {
            "content-type": "application/json",
            "api-key": "3c3640c38eeb477192ad99b96fce26b4"
        }
    elif llm_name in ['claude-instant-1', 'claude-2']:
        url = "https://openxlab.org.cn/gw/alles-apin-hub/v1/claude/v1/text/chat"
        headers = {
            "content-type": "application/json",
            "alles-apin-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxNiwidXNlcm5hbWUiOiJsYW50aWFuIiwiYXBwbHlfYXQiOjE2OTAxOTEwNTQxMjYsImV4cCI6MTg3MTYzMTA1NH0.XoYqnBY7bmzGNVSEmhPcHKWByjmslsZ2tvV9mceuJaw"
        }
    for retry_i in range(retry_num):
        if llm_name in ['gpt-4', 'gpt-4-1106-preview', 'gpt-4o']:
            input_data = _prepare_input(payload, temp, max_tokens, llm_name)
            try:
                data = requests.post(url, headers=headers, data=json.dumps(input_data), timeout=200)
                response = data.json()['choices'][0]['message']['content']
                prompt_tokens = data.json()['usage']['prompt_tokens']
                completion_tokens = data.json()['usage']['completion_tokens']
                sys.stdout.flush()
            except requests.exceptions.Timeout as errt:
                print(f'Exceed timeout error for {llm_name}:', errt)
                continue
            except Exception as error:
                print(f'[!] meet strange error:', error)
                print(data.text)
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
                continue

            if 'Rate limit reached for' in response:
                print(f'[!] You achieve the rate limit for {llm_name}, please sleep for 15 seconds')
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
            elif 'Error code' in response:
                print(f'[!] meet the error code for {llm_name}:', response)
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
            elif 'Bad gateway' in response:
                print(f'[!] Bad gateway occur, please sleep for 15 seconds for {llm_name}')
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
            elif response.startswith('\n<html><head>\n<meta type=\"copyright\" content=\"Copyright (C) 1996-2020 '):
                print(f'[!] GPT-4 turbo face the error, sleep 15 seconds')
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
            elif 'HTTPSConnectionPool' in response:
                print(f'[!] generation contains the HTTPS error in gpt-4 response')
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
            elif 'You exceeded your current quota' in response:
                print(f'[!] You exceeded your current quota for {llm_name}, please sleep for 15 seconds')
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
            elif len(response) == 0:
                print(f'[!] find no response from the API for {llm_name}')
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
            elif 'The server had an error while processing your request' in response:
                print(f'[!] The server had an error while processing your request for {llm_name}')
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
            elif 'Request timed out' in response:
                print(f'[!] meet request time out error for gpt-4, sleep 15 seconds')
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
            elif 'Alles-APIN' in response:
                print(f'[!] meet the APIN error for {llm_name}: {response}')
                sys.stdout.flush()
                time.sleep(10 + 20 * random.random())
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
                # print('Exceed timeout error for {llm_name}:', errt, data.text)
                print('Exceed timeout error for {llm_name}:', errt)
                sys.stdout.flush()
                time.sleep(5)
                continue
            except Exception as e:
                try:
                    print(f'[!] Error for Claude:',  e, data.text)
                    sys.stdout.flush()
                    if 'This request is blocked by Alles-APIN due to request rate limited' in data.text:
                        print(f'[!] Claude meet the error:', 'This request is blocked by Alles-APIN due to request rate limite')
                        sys.stdout.flush()
                    time.sleep(5)
                except:
                    print(f'[!] Error for Claude:',  e)
                    
        time_acc += 5
        print(f'>>> retry time >>>', retry_i)
    return None, 0, 0, index

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


def set_proxy():
    http_proxy = 'https://lantian:5trslplFamkoYwSb6Lk8TpwwpU2Tm1TWZDxf48k1OxzZsVAKo41GBgorgHaD@aliyun-proxy.pjlab.org.cn:13128'
    https_proxy = 'https://lantian:5trslplFamkoYwSb6Lk8TpwwpU2Tm1TWZDxf48k1OxzZsVAKo41GBgorgHaD@aliyun-proxy.pjlab.org.cn:13128'
    HTTP_PROXY = 'https://lantian:5trslplFamkoYwSb6Lk8TpwwpU2Tm1TWZDxf48k1OxzZsVAKo41GBgorgHaD@aliyun-proxy.pjlab.org.cn:13128'
    HTTPS_PROXY = 'https://lantian:5trslplFamkoYwSb6Lk8TpwwpU2Tm1TWZDxf48k1OxzZsVAKo41GBgorgHaD@aliyun-proxy.pjlab.org.cn:13128'
    if os.getenv('http_proxy') == http_proxy:
        pass
    else:
        os.environ['http_proxy'] = http_proxy
    if os.getenv('https_proxy') == https_proxy:
        pass
    else:
        os.environ['https_proxy'] = https_proxy
    if os.getenv('HTTP_PROXY') == HTTP_PROXY:
        pass
    else:
        os.environ['HTTP_PROXY'] = HTTP_PROXY 
    if os.getenv('HTTPS_PROXY') == HTTPS_PROXY:
        pass
    else:
        os.environ['HTTPS_PROXY'] = HTTPS_PROXY
    # os.system(f"export http_proxy={http_proxy}")
    # os.system(f"export https_proxy={https_proxy}")
    # os.system(f"export HTTP_PROXY={HTTP_PROXY}")
    # os.system(f"export HTTPS_PROXY={HTTPS_PROXY}")


def batch_chat(payloads, sleep_time=20, retry_num=5, temp=0.5, max_tokens=4096, model_name='gpt-4-1106-preview', debug=False):
    #if model_name in ['gpt-4-1106-preview', 'gpt-4o']:
    #    set_proxy()
    if debug is True:
        for index, payload in enumerate(payloads):
            # _chat_one_session_azure(payload, sleep_time, retry_num, temp, max_tokens, model_name, index)
            #_chat_one_session_openai(payload, sleep_time, retry_num, temp, max_tokens, model_name, index)
            _chat_one_session_personal(payload, sleep_time, retry_num, temp, max_tokens, model_name, index)
    else:
        pool = Pool(processes=32)
        result_list = []
        for index, payload in enumerate(payloads):
            # result_list.append(pool.apply_async(_chat_one_session_azure, (payload, sleep_time, retry_num, temp, max_tokens, model_name, index)))
            result_list.append(pool.apply_async(_chat_one_session_personal, (payload, sleep_time, retry_num, temp, max_tokens, model_name, index)))
        pool.close()
        pool.join()
        values = [rest.get() for rest in result_list]
        sorted_values = sorted(values, key=lambda x:x[-1])
        # sorted_values = [(i[0], i[1], i[2], i[3]) for i in sorted_values]
        sorted_values = [i[0] for i in sorted_values]
        return sorted_values


def batch_chat_lagent_gptapi(payloads, sleep_time=20, retry_num=5, temp=0.5, max_tokens=4096, model_name='gpt-4-1106-preview', debug=False):
    #if model_name in ['gpt-4-1106-preview', 'gpt-4o']:
    #    set_proxy()
    if debug is True:
        responses = []
        for index, payload in enumerate(payloads):
            ipdb.set_trace()
            response = lagent_gptapi.chat([payload])
            responses.append(response)
    else:
        try:
            result_list = lagent_gptapi.chat(payloads)
        except:
            result_list = []
            for payload in payloads:
                try:
                    rest = lagent_gptapi.chat(payload)
                except Exception as error:
                    print(f'[!] Meet one error:', error)
                    #ipdb.set_trace()
                    rest = ''
                result_list.append(rest)
        return result_list


if __name__ == "__main__":
    llm_name = 'gpt-4-1106-preview'
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
            #{
            #    'model': llm_name,
            #    'messages': [
            #        {
            #            'role': 'user',
            #            'content': '你是谁'
            #        }    
            #    ]
            #},
            #[
            #    {
            #        'role': 'user',
            #        'content': 'mysql数据库如何插入数据的时候如何强制使用之前删除留下的剩余空间呢'
            #    }
            #],
        ],
        temp=0,
        model_name=llm_name,
        debug=False
    )
    print(response)

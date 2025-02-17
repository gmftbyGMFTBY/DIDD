import json
import pprint
import numpy as np
import ipdb
import tiktoken
import os


def extract_domain(string):
    if 'chat' in string:
        return 'chat'
    elif 'qa' in string:
        return 'qa'
    elif 'harmlessness' in string:
        return 'harmlessness'
    elif 'summary' in string:
        return 'summary'
    elif 'translate' in string:
        return 'translate'
    elif 'math_cot' in string:
        return 'math_cot'
    elif 'math_pot' in string:
        return 'math_pot'
    elif 'code_exec' in string:
        return 'code_exec'
    elif 'code_not_exec' in string:
        return 'code_not_exec'
    else:
        raise Exception(f'[!] Unknown domain:', string)

root = '20240704_resumm_test'

price = {
    'in': 10/1000000,
    'out': 30/1000000
}

cost_in = {
    'translate': [],
    'chat': [],
    'harmlessness': [],
    'qa': [],
    'summary': [],
    'math_cot': [],
    'math_pot': [],
    'code_exec': [],
    'code_not_exec': []
}

cost_out = {
    'translate': [],
    'chat': [],
    'harmlessness': [],
    'qa': [],
    'summary': [],
    'math_cot': [],
    'math_pot': [],
    'code_exec': [],
    'code_not_exec': []
}



encoding = tiktoken.get_encoding("cl100k_base")

for folder in os.listdir(root):
    for file in os.listdir(os.path.join(root, folder)):
        path = os.path.join(root, folder, file)
        domain = extract_domain(file)
        with open(path) as f:
            data = [json.loads(line) for line in f.readlines()]
            data_count_out = [len(encoding.encode(item['evaluation']['cot'])) for item in data if type(item['evaluation']['cot']) == str]
            data_count_in = [len(encoding.encode(item['question'])) + len(encoding.encode(item['generation'])) + len(encoding.encode(item['feedback'])) * 2 for item in data]
            #if len(data_count_out) < len(data):
            #    ipdb.set_trace()
        # ipdb.set_trace()
        cost_in[domain].append(sum(data_count_in))
        cost_out[domain].append(sum(data_count_out))

prices = {key: 0 for key in cost_in}
for domain in cost_in:
    token_in = np.mean(cost_in[domain]) * price['in']
    token_out = np.mean(cost_out[domain]) * price['out']
    prices[domain] = token_in + token_out

pprint.pprint(prices)
print(sum(prices.values()))

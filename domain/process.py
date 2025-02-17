import json
from itertools import chain
from copy import deepcopy
import re
import random
from tqdm import tqdm
import os
from collections import Counter
import ipdb



def remove_labels(string):
    new_string = re.sub(r'\[S\d+\]', '', string)
    return new_string

def convert(item):
    conversation_input = '\n'.join([f'["Begin of Utterance"] {utterance["role"]}: {utterance["content"]} [End of Utterance]' for utterance in item['input'] + [{'role': 'assistant', 'content': item['response']}]])
    conversation = [{'input': conversation_input, 'output': item['critique'][-1]}]
    return conversation


def mapping_to_domain(string):
    string = string.lower()
    if 'math' in string or 'code' in string or 'coding' in string:
        return 'math_code'
    elif string in ['text_to_text_translation', 'text_summarization', 'summarization', 'post_summarization', 'note_summarization']:
        return 'translation_summarization'
    elif string in ['chitchat', 'open_question', 'creative_writing']:
        return 'chat_qa'
    else:
        return None


if __name__ == "__main__":
    random.seed(0)
    prompt = open('prompts/singlewise_critique.md').read()

    file = '../multicritique_sft/train.jsonl'

    pbar = tqdm(total=64804)
    new_data = {}
    with open(file) as f:
        for line in f:
            item = json.loads(line)
            category = mapping_to_domain(item['key_name'])
            if category is None:
                continue
            if category not in new_data:
                new_data[category] = []
            quality = item['evaluated_response_quality']
            ipt = item['input']
            response = item['responses'][quality]
            critique = item['parse_final_feedbacks']
            score = item['parse_final_judgement_score']
            new_data[category].append({
                'input': ipt,
                'response': response,
                'critique': critique,
                'score': score
            })
            pbar.update(1)

    datasets = []
    max_base_num = 3000
    for key in ['translation_summarization', 'chat_qa', 'math_code']:
        data = []
        for sample in new_data[key]:
            conv = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in sample['input']]) + ' [end of conversation]'
            string = prompt.format(conversation=conv, response=remove_labels(response))
            data.append({'conversation': [{'input': string, 'output': sample['critique'][-1]}]})
        datasets.append(data)
        with open(f'data/{key}.json', 'w') as f:
            dd = random.sample(data, min(max_base_num, len(data)))
            json.dump(dd, f, ensure_ascii=False, indent=4)
        print(f'[!] {key}:', len(dd))

    max_length = max([len(data) for data in datasets]) // 3 + 20
    overall = []
    for data in datasets:
        overall.extend(random.sample(data, min(max_length, len(data))))
    with open(f'data/overall.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f'[!] overall:', len(overall))

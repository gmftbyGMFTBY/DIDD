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


if __name__ == "__main__":
    random.seed(0)

    file = '../multicritique_sft/train.jsonl'

    pbar = tqdm(total=64804)
    new_data = {}
    with open(file) as f:
        for line in f:
            item = json.loads(line)
            string = '\n'.join([utterance['content'] for utterance in item['input']])
            if string not in new_data:
                new_data[string] = {}

            #quality = item['evaluated_response_quality']
            ipt = item['input']
            response = item['responses'][quality]
            critique = item['parse_final_feedbacks']
            score = item['parse_final_judgement_score']
            score = round(score)
            if 1 <= score <= 3:
                quality = 'low'
            elif 4 <= score <= 6:
                quality = 'medium'
            else:
                quality = 'high'
            new_data[string][quality] = {
                'input': ipt,
                'response': response,
                'critique': critique,
                'score': score
            }
            pbar.update(1)

    processed_data = {}
    for key, value in new_data.items():
        if len(value) == 3 and 'low' in value and 'medium' in value and 'high' in value:
            low_score = value['low']['score']
            medium_score = value['medium']['score']
            high_score = value['high']['score']
            if low_score < medium_score < high_score:
                processed_data[key] = value

    print(len(processed_data))

    with open('filtered_data.json', 'w') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

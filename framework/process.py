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
    prompt = open('prompts/singlewise_critique.md').read()

    file = '../multicritique_sft/train.jsonl'

    pbar = tqdm(total=64804)
    new_data = []
    few_shot = {}
    with open(file) as f:
        for line in f:
            item = json.loads(line)
            quality = item['evaluated_response_quality']
            category = item['key_name']
            if category not in few_shot:
                few_shot[category] = {}
            if quality not in few_shot[category]:
                few_shot[category][quality] = []
            ipt = item['input']
            response = item['responses'][quality]
            critique = item['parse_final_feedbacks']
            score = item['parse_final_judgement_score']
            new_data.append({
                'input': ipt,
                'response': response,
                'critique': critique,
                'score': score
            })
            few_shot[category][quality].append(new_data[-1])
            pbar.update(1)

    dataset = []
    for sample in random.sample(new_data, 3000):
        ipt = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in sample['input']]) + ' [end of conversation]'
        string = prompt.format(conversation=ipt, response=remove_labels(sample['response']))
        conv = {'conversation': [{'input': string, 'output': sample['critique'][-1]}]}
        dataset.append(conv)

    with open('data/baseline.json', 'w') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)

    print(f'[!] total category:', len(few_shot))
    #### save the few-shot
    
    few_shot_num = 10
    new_few_shot = {}
    random.seed(0)
    for category in few_shot:
        new_few_shot[category] = {}
        for quality in few_shot[category]:
            new_few_shot[category][quality] = random.sample(few_shot[category][quality], min(few_shot_num, len(few_shot[category][quality])))

    with open('gpt4_generation/few_shot.json', 'w') as f:
        json.dump(new_few_shot, f, ensure_ascii=False, indent=4)

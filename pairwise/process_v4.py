import json
import numpy as np
from tqdm import tqdm
import ipdb
import random

random.seed(0)

'''分析 high-low，medium-low，high-low 的重要性'''


if __name__ == "__main__":
    file = '../multicritique_sft/train.jsonl'
    pbar = tqdm(total=64804)
    new_data = {}
    with open(file) as f:
        for line in f:
            item = json.loads(line)
            query = '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in item['input']])
            if query not in new_data:
                new_data[query] = {}

            quality = item['evaluated_response_quality']
            ipt = item['input']
            response = item['responses'][quality]
            critique = item['parse_final_feedbacks']
            score = round(item['parse_final_judgement_score'])
            new_data[query][quality] = {
                'input': ipt,
                'response': response,
                'critique': critique,
                'score': score,
            }
            pbar.update(1)
    #########

    file = 'filtered_data_processed.json'
    prompt = open('prompts/pairwise_critique.md').read()
    with open(file) as f:
        data = json.load(f)

    overall =  []
    easy, hard_1, hard_2 = [], [], []
    for _, value in data.items():
        ex_samples = []
        for mode, sample in value.items():
            if 'conv' not in sample:
                continue
            conv = sample['conv']
            query = sample['query']
            assert len(conv) == 2
            ipt, opt = conv[0]['content'], conv[1]['content']
            if opt:
                if mode == 'low-high':
                    low_score, high_score = new_data[query]['low']['score'], new_data[query]['high']['score']
                    easy.append({'conversation': [{'input': ipt, 'output': opt}]})
                elif mode == 'low-medium':
                    low_score, medium_score = new_data[query]['low']['score'], new_data[query]['medium']['score']
                    hard_1.append({'conversation': [{'input': ipt, 'output': opt}]})
                elif mode == 'medium-high':
                    medium_score, high_score = new_data[query]['medium']['score'], new_data[query]['high']['score']
                    hard_2.append({'conversation': [{'input': ipt, 'output': opt}]})
    overall_random_baseline_5000 = random.sample(easy + hard_1 + hard_2, 5000)
    print(f'[!] {len(easy)}; {len(hard_1)}; {len(hard_2)}; {len(overall)};')
    with open('data/baseline_comp_num_5000.json', 'w') as f:
        json.dump(overall_random_baseline_5000, f, ensure_ascii=False)

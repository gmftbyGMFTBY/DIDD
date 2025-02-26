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

    easy, hard_1, hard_2, overall = [], [], [], []
    overall_dis =  []
    all_ = []
    for _, value in data.items():
        ex_samples = []
        for mode, sample in value.items():
            if mode in ['dataset_name', 'key_name']:
                continue
            conv = sample['conv']
            query = sample['query']
            assert len(conv) == 2
            ipt, opt = conv[0]['content'], conv[1]['content']
            if opt:
                if mode == 'low-high':
                    low_score, high_score = new_data[query]['low']['score'], new_data[query]['high']['score']
                    if low_score <= 3 and high_score >= 7:
                        easy.append({'conversation': [{'input': ipt, 'output': opt}]})
                        ex_samples.append(easy[-1])
                elif mode == 'low-medium':
                    low_score, medium_score = new_data[query]['low']['score'], new_data[query]['medium']['score']
                    if low_score <= 3 and 3 < medium_score < 7:
                        hard_1.append({'conversation': [{'input': ipt, 'output': opt}]})
                        ex_samples.append(hard_1[-1])
                elif mode == 'medium-high':
                    medium_score, high_score = new_data[query]['medium']['score'], new_data[query]['high']['score']
                    if 3<= medium_score < 7 and high_score >= 7:
                        hard_2.append({'conversation': [{'input': ipt, 'output': opt}]})
                        ex_samples.append(hard_2[-1])
    rates = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    num_sample = len(hard_2)
    others = easy + hard_1
    for rate in rates:
        num_a, num_b = int(num_sample * rate), int(num_sample * (1-rate))
        s = random.sample(hard_2, num_a)
        s.extend(random.sample(others, num_b))
        with open(f'data/hard_2_rate_exp_{rate}.json', 'w') as f:
            json.dump(s, f, ensure_ascii=False, indent=4)
        print(f'[!] save {len(s)} samples')



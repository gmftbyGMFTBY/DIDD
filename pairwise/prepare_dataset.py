import json
import ipdb
import random

random.seed(0)



if __name__ == "__main__":
    file = 'filtered_data_processed.json'
    prompt = open('prompts/pairwise_critique.md').read()
    with open(file) as f:
        data = json.load(f)

    easy, hard_1, hard_2, overall = [], [], [], []
    for _, value in data.items():
        for mode, sample in value.items():
            if mode in ['dataset_name', 'key_name']:
                continue
            conv = sample['conv']
            assert len(conv) == 2
            ipt, opt = conv[0]['content'], conv[1]['content']
            if opt:
                if mode == 'low-high':
                    easy.append({'conversation': [{'input': ipt, 'output': opt}]})
                elif mode == 'low-medium':
                    hard_1.append({'conversation': [{'input': ipt, 'output': opt}]})
                elif mode == 'medium-high':
                    hard_2.append({'conversation': [{'input': ipt, 'output': opt}]})

        random_ = random.random()
        if random_ < 0.333333:
            overall.append(easy[-1])
        elif 0.333333 < random_ < 0.666666:
            overall.append(hard_1[-1])
        else:
            overall.append(hard_2[-1])

    print(f'[!] {len(easy)}; {len(hard_1)}; {len(hard_2)}; {len(overall)}')

    with open('data/easy.json', 'w') as f:
        json.dump(easy, f, ensure_ascii=False)
    with open('data/hard_1.json', 'w') as f:
        json.dump(hard_1, f, ensure_ascii=False)
    with open('data/hard_2.json', 'w') as f:
        json.dump(hard_2, f, ensure_ascii=False)
    with open('data/overall.json', 'w') as f:
        json.dump(overall, f, ensure_ascii=False)

import json
import os
import numpy as np
from tqdm import tqdm
import ipdb
import random

random.seed(0)

'''pairwise在domain下的分析'''


if __name__ == "__main__":
    data = []
    for file in os.listdir('output'):
        conv = json.load(open(os.path.join('output', file)))['conv']
        data.append({'conversation': [{'input': conv[0]['content'], 'output': conv[1]['content']}]})
    print(f'[!] collect {len(data)} samples')
    for num in [1000, 2000, 4000, 5000, 6000, 7000, 8000]:
        samples = random.sample(data, num)
        with open(f'data/baseline_train_num_{num}.json', 'w') as f:
            json.dump(samples, f, ensure_ascii=False)

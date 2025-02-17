import json
import pprint
import numpy as np
from collections import Counter
import ipdb
import re
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--topk", default=50, type=int)
parser.add_argument("--root-path", default='output')
parser.add_argument("--iter-num", default=0, type=int)
args = parser.parse_args()


if __name__ == "__main__":
    labels, save_category, save_quality, save = [], {}, {}, {}
    for file in os.listdir(f'{args.root_path}/iter_{args.iter_num}/meta_evaluation'):
        nn = file.strip('.json').split('_')
        index = nn[0]
        quality = nn[-1]
        category = '_'.join(nn[1:-1])
        path = os.path.join(f'{args.root_path}/iter_{args.iter_num}/meta_evaluation', file)
        data = json.load(open(path))[-1]['content']
        parses = re.findall(r'Quality.*(\d)', data, re.DOTALL | re.MULTILINE)
        if len(parses) > 0:
            labels.append(int(parses[-1]))
            if category not in save_category:
                save_category[category] = [labels[-1]]
            else:
                save_category[category].append(labels[-1])

            if quality not in save_quality:
                save_quality[quality] = [labels[-1]]
            else:
                save_quality[quality].append(labels[-1])

            key = f'{category}-{quality}'
            if key not in save:
                save[key] = [labels[-1]]
            else:
                save[key].append(labels[-1])

    print(Counter(labels).most_common())
    for key, value in save_quality.items():
        print(f'[!] {key}:', np.mean(value))

    #results = [(key, float(np.mean(value))) for key, value in save_category.items()]
    #results = sorted(results, key=lambda x: float(x[1]))
    results = [(key, float(np.mean(value))) for key, value in save.items()]
    results = sorted(results, key=lambda x: float(x[1]))
    first_corr_index = 0
    for index, result in enumerate(results):
        if result[1] == 1.0:
            first_corr_index = index
            break
    topk = min(args.topk, first_corr_index)
    print(f'[!] first_corr_index: {first_corr_index}; topk:', topk)
    with open(f'{args.root_path}/iter_{args.iter_num}/top-{topk}-failure-dis.json', 'w') as f:
        json.dump(results[:topk], f, ensure_ascii=False, indent=4)




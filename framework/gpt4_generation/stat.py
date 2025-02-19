import json
import pprint
import numpy as np
from collections import Counter
import ipdb
import re
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--root-path", default='output')
# mode 1: origin distribution
# mode 2: new distribution
# mode 3: mixuture distribution
parser.add_argument("--mode", default='output')
parser.add_argument("--iter-num", default=0, type=int)
args = parser.parse_args()


if __name__ == "__main__":

    raw_domain_dis = {
        # iter-1: 0.7
        'general_communication': 0.175,
        'creative_writing': 0.175,
        'nlp_tasks': 0.175,
        'summarization': 0.175,
        # tier-2: 0.2
        'code': 0.1,
        'exam_question': 0.1,
        # iter-3: 0.1
        'functional_writing': 0.05,
        'rewriting': 0.05,
    }
    raw_quality_dis = {'high': 0.3, 'medium': 0.6, 'low': 0.1}

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

    qualities_dis = sorted([(key, 1-np.mean(value).item()) for key, value in save_quality.items()], key=lambda x: x[1])
    domains_dis = sorted([(key, 1-np.mean(value).item()) for key, value in save_category.items()], key=lambda x: x[1])

    overall_rate = sum([a for _, a in qualities_dis])
    qualities_dis = [(a, b/overall_rate) for a, b in qualities_dis]

    overall_rate = sum([a for _, a in domains_dis])
    domains_dis = [(a, b/overall_rate) for a, b in domains_dis]

    qualities_dis = {key: value for key, value in qualities_dis}
    domains_dis = {key: value for key, value in domains_dis}

    alpha = 0.5
    fq_dis = {}
    for key in qualities_dis:
        v = qualities_dis[key]
        v_ = raw_quality_dis[key]
        fq_dis[key] = alpha * v + (1 - alpha) * v_
    fd_dis = {}
    for key in domains_dis:
        v = domains_dis[key]
        v_ = raw_domain_dis[key]
        fd_dis[key] = alpha * v + (1 - alpha) * v_

    with open(f'{args.root_path}/iter_{args.iter_num}/failure-dis.json', 'w') as f:
        json.dump({'domain_dis': fd_dis, 'quality_dis': fq_dis}, f, ensure_ascii=False, indent=4)

import json
import numpy as np
from collections import Counter
import ipdb
import re

if __name__ == "__main__":
    file = 'data/baseline_iter_0.json'
    with open(file) as f:
        data = json.load(f)

    scores = []
    for sample in data:
        content = sample['conversation'][0]['output']
        score = re.findall(".*Score: (\d+\.\d+|\d+)", content)
        if len(score) > 0:
            score = float(score[-1])
            scores.append(score)
    print('max:', max(scores))
    print('min:', min(scores))
    print('avg:', np.mean(scores))
    print(sorted(Counter(scores).most_common(), key=lambda x:x[0]))

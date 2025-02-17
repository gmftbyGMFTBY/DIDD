import json
import os

samples = {}
for file in os.listdir('data'):
    path = os.path.join('data', file)
    data = json.load(open(path))
    category = data[-1]
    detail = data[-2]['content']
    samples[category] = detail


with open('few_shot_detail.json', 'w') as f:
    json.dump(samples, f, ensure_ascii=False, indent=4)

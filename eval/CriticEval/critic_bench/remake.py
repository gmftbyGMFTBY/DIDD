import os
import re
import json
import ipdb

root = '20240724_s2_resumm_evaluation_cache'
root_new = '20240724_s2_resumm_evaluation_cache_converted'
if os.path.exists(root_new) is False:
    os.makedirs(root_new)

for folder in os.listdir(root):
    #if '359_hf_ckpt' not in folder:
    #    continue

    if os.path.exists(os.path.join(root_new, folder)) is False:
        os.makedirs(os.path.join(root_new, folder))

    for file in os.listdir(os.path.join(root, folder)):
        path = os.path.join(root, folder, file)
        with open(path) as f:
            data = [json.loads(line) for line in f.readlines()]

        new = []
        for item in data:
            evaluation = item['evaluation']['cot']
            try:
                scores = re.findall('Score: (\d+\.\d+|\d+)', evaluation)
                score = float(scores[0])
            except:
                score = 0

            item['evaluation']['score'] = score
            new.append(item)

        with open(os.path.join(root_new, folder, file), 'w') as f:
            for item in new:
                f.write(json.dumps(item, ensure_ascii=False) + '\n')

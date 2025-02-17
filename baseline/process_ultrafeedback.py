import json
import os
import re
import ipdb
import random



if __name__ == "__main__":
    root_path = '/home/lt/openbmb/UltraFeedback'
    prompt = open('prompts/singlewise_critique.md').read()
    dataset = []
    sample_num = 2000
    for file in os.listdir(root_path):
        if file.endswith('jsonl'):
            path = os.path.join(root_path, file)
            subdata = [json.loads(line) for line in open(path).readlines()]
            for sample in subdata:
                instruction = sample['instruction']
                for completion in sample['completions']:
                    response = completion['response']
                    critique = completion['critique']
                    score = completion['fine-grained_score']

                    query = '[begin of conversation] user: ' + instruction + ' [end of conversation]'
                    critique += f'# Final Judgement\nScore: {score}'
                    string = prompt.format(conversation=query, response=response)
                    dataset.append({'conversation': [{'input': string, 'output': critique}]})

    random.seed(0)
    dataset = random.sample(dataset, sample_num)

    with open('data/ultracm_ours.json', 'w') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)
        print(f'[!] collect {len(dataset)} samples for training')


from data_generation import parse_test_set
import os
import json, ipdb

if __name__ == "__main__":

    prompt = open('prompts/pairwise_critique.md').read()

    for folder in os.listdir('output'):
        data = []
        for file in os.listdir(os.path.join('output', folder)):
            d = json.load(open(os.path.join('output', folder, file)))
            samples = parse_test_set(d)
            for sample in samples:
                input = [{'role': 'user', 'content': sample['query']}]
                string = prompt.format(conversation=input, responsea=sample['responsea'], responseb=sample['responseb'])
                conv = {'conversation': [{'input': string, 'output': sample['critique']}]}
                data.append(conv)
        print(f'[!] found {len(data)} samples under {folder}')

        with open(f'{folder}.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

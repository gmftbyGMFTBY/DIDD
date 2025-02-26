import json
import re
import ipdb



if __name__ == "__main__":
    data = json.load(open('data/autoj.json'))
    dataset = []
    prompt = open('prompts/pairwise_critique.md').read()
    for sample in data:
        input = sample['conversation'][0]['input']
        output = sample['conversation'][0]['output']
        content = re.findall('\[BEGIN DATA\](.+)\[END DATA\]', input, re.DOTALL | re.MULTILINE)
        assert len(content) == 1
        content = content[0]

        if '[Response 1]' not in content:
            continue

        # parse query
        query = re.findall('\[Query\]:(.+)\[Response 1\]', content, re.DOTALL | re.MULTILINE)
        assert len(query) == 1
        query = query[0].strip().strip('***').strip()
        query = '[begin of conversation] user: ' + query + ' [end of conversation]'

        # parse response 1
        response_1 = re.findall('\[Response 1\]:(.+)', content, re.DOTALL | re.MULTILINE)
        assert len(response_1) == 1
        response_1 = response_1[0].strip().strip('***').strip()

        # parse response 2
        response_2 = re.findall('\[Response 2\]:(.+)', content, re.DOTALL | re.MULTILINE)
        assert len(response_2) == 1
        response_2 = response_2[0].strip().strip('***').strip()

        # parse critique
        results = output.split('2. The final decision:')
        try:
            assert len(results) == 2
        except:
            continue

        score = re.findall('the final decision is Response (\d)', output, re.DOTALL | re.MULTILINE)
        try:
            assert len(score) == 1
        except:
            continue
        if score[0] == '1':
            score = 'A'
        elif score[0] == '2':
            score = 'B'
        pattern = f' Label: {score}'
        new_output = results[0].strip() + pattern
        string = prompt.format(conversation=query, responsea=response_1, responseb=response_2)
        dataset.append({'conversation': [{'input': string, 'output': new_output}]})

    with open('data/autoj_ours_pairiwise.json', 'w') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)
        print(f'[!] collect {len(dataset)} samples for training')


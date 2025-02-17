import json
import re
import ipdb



if __name__ == "__main__":
    data = json.load(open('data/autoj.json'))
    dataset = []
    prompt = open('prompts/singlewise_critique.md').read()
    for sample in data:
        input = sample['conversation'][0]['input']
        output = sample['conversation'][0]['output']
        content = re.findall('\[BEGIN DATA\](.+)\[END DATA\]', input, re.DOTALL | re.MULTILINE)
        assert len(content) == 1
        content = content[0]

        if '[Response 1]' in content:
            continue

        # parse query
        query = re.findall('\[Query\]:(.+)\[Response\]', content, re.DOTALL | re.MULTILINE)
        assert len(query) == 1
        query = query[0].strip().strip('***').strip()
        query = '[begin of conversation] user: ' + query + ' [end of conversation]'

        # parse response
        response = re.findall('\[Response\]:(.+)', content, re.DOTALL | re.MULTILINE)
        assert len(response) == 1
        response = response[0].strip().strip('***').strip()

        # parse critique
        score = re.findall('Rating: \[\[(\d+\.\d+|\d+)\]\]', output, re.DOTALL | re.MULTILINE)
        assert len(score) == 1
        pattern = f'Rating: [[{score[0]}]]'
        new_output = output.replace(pattern, '') + f'# Final Judgement\nScore: {score[0]}'

        string = prompt.format(conversation=query, response=response)
        dataset.append({'conversation': [{'input': string, 'output': new_output}]})

    with open('data/autoj_ours.json', 'w') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4)
        print(f'[!] collect {len(dataset)} samples for training')


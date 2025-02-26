import re
import os
from copy import deepcopy
try:
    from .exec import *
except:
    pass
import yaml
from yamlinclude import YamlIncludeConstructor
YamlIncludeConstructor.add_to_loader_class(loader_class=yaml.FullLoader)



def segment_response(response, min_length=3, criteria_type=''):
    """segment the input response and add the citation box brackets
    Refer to: https://arxiv.org/pdf/2305.14627.pdf
    
    we segment the response with the sentence boundary

    如果是代码题，那么下面的匹配规则可能有问题
    """
    
    coding_criteria_types = set([
        'code_simplification',
        'code_generation',
        'explaining_code',
        'code_correction_rewriting',
        'code_to_code_translation',
        'airoboro2.2_coding'
    ])
    if criteria_type in coding_criteria_types:
        # use the \n as the separator
        segments = re.split(r'(\n+)', response)
        index = 1
        strings = []
        for segment in segments:
            if segment.strip():
                # pure text
                if segment[-1] in '.?!;:,+-*~!。，：！？':
                    segment_ = segment[:-1] + f" [S{index}]{segment[-1]}"
                else:
                    segment_ = segment + f" [S{index}]"
                strings.append(segment_)
                index += 1
            else:
                strings.append(segment)
        new_response = ''.join(strings)
    else:
        response += ' '    # 兼容如下的正则表达式中的空白符号匹配
        # ignore the enumeration like "1. ...; 2. ...;"
        segments = re.split(r'([\.?!;]\s)', response)
        # segments = re.split(r'(?<=[^A-Z].[.?]) +(?=[A-Z])', response)
        segments = [segment for segment in segments if segment.strip()]
        # add the brackets sequentially
        index = 1
        if len(segments) == 1:
            # no punctation, just add the brackets in the end
            new_response = f'{segments[0]} [S{index}]'
            index += 1
        else:
            strings = []
            for segment in segments:
                if segment[0] in '.?!;':
                    if len(strings) == 0:
                        strings.append(segment)
                    elif len(strings[-1].strip()) >= min_length:
                        # effective citation
                        segment = f" [S{index}]{segment}"
                        strings.append(segment)
                        index += 1
                    else:
                        strings[-1] += segment
                else:
                    strings.append(segment)
                    
            if strings[-1].strip()[-1] not in '.?!;':
                strings[-1] = strings[-1].strip() + f" [S{index}]"
            new_response = ''.join(strings)
        try:
            assert index > 1
        except:
            if new_response.endswith('.') or new_response.endswith('?') or new_response.endswith('!') or new_response.endswith(';'):
                punc = new_response[-1]
                new_response = new_response[:-1] + f' [S1]{punc}'
            else:
                new_response += f' [S1].'
    # print(new_response)
    # exit()
    return new_response


def get_exec_rest(code, unit_test, data_source):
    code = code + unit_test
    if data_source == 'humaneval':
        function_name = find_fist_function_name(code)
        code += f'\ncheck({function_name})'
    exec_rest = exec_code_no_unit_test(code)
    return exec_rest['detail']


def clean_translation(string):
    string = string.replace('来源（en）：', '')
    string = string.replace('来源：', '')
    string = string.replace('来源（英）：', '')
    string = string.replace('来源：（英）', '')
    string = string.replace('源 (en):', '')
    return string

# for humaneval dataset
def find_fist_function_name(string):
    try:
        index = string.index('def ')
        function_name = string[index:].split('\n')[0]
        f_index = function_name.index('(')
        function_name = function_name[:f_index].replace('def', '').strip()
    except:
        index = string.index('assert ')
        function_name = string[index:].split('\n')[0]
        f_index = function_name.index('(')
        function_name = function_name[:f_index].replace('assert', '').strip()
    return function_name



def extract_decision(string):
    try:
        try:
            decision = re.findall('.*(Decision: .+)', string)[0].replace('Decision:', '').strip()
            decision = float(decision)
        except:
            try:
                decision = float(decision.split()[0])
            except:
                decision = parse_math_result(string)
    except:
        decision = None
    return decision


def extract_decision_option(string):
    try:
        decision = re.findall('.*(Decision: .+)', string)[0].replace('Decision:', '').strip()
    except:
        decision = string.replace('.', '').strip()
    return decision

    
def extract_likert(string):
    decision = re.findall('.*(Likert: .+)', string)[0].replace('Likert:', '').strip()
    try:
        decision = int(decision[0])
    except:
        decision = ''
    return decision


'''
def parse_math_result(string):
    try:
        decision = re.findall('.*(#### .+)', string)[0].replace('####', '').strip()
    except:
        return ''
    # decision = decision.replace('RESULT:', '').strip()
    predictions = decision.split()
    res = None
    for v in predictions:
        try:
            if eval(v):
                if type(eval(v)) == float or type(eval(v)) == int:
                    res = eval(v)
                    break
        except:
            pass
    if res:
        decision = res
    else:
        decision = ''
    return decision
'''
def parse_math_result(string):
    '''最终答案肯定在后面，我们从后面parse数字即可'''
    try:
        res = None
        for v in reversed(string.split()):
            try:
                if eval(v):
                    if type(eval(v)) == float or type(eval(v)) == int:
                        res = eval(v)
                        break
            except:
                pass
        if res:
            decision = res
        else:
            decision = ''
    except:
        return ''
    return decision


def parse_code(code, lang='json'):
    pattern = rf'```{lang}.*?\s+(.*?)```'
    match = re.search(pattern, code, re.DOTALL)
    if match:
        code_ = match.group(1)
        try:
            code_item = json.loads(code_)
        except:
            print(f'[!] {code_} is not valid in JSON format')
            code_item = []
    else:
        if '```json' in code:
            code.replace('```json', '')
        if '```' in code:
            code.replace('```', '')
        try:
            code_item = json.loads(code)
        except:
            print(f'[!] {code} is not valid in JSON format')
            code_item = []
    return code_item


def read_yaml(category, max_num=100, with_degree=False):
    """
    # List of Criteria
// a block for one criteria consisting of description and degree (significance), variable in `{{}}` should be replaced. Keep output following struture in order
## {{Name of First Criteria}}
// a string of the description and details of criteria
Description: {{description}}
// a word reflects the significance of criteria, select degree from three types (least to most significance): (1) normal; (2) medium; (3) important
Degree: {{degree}}


**with_degree** controls whether we include the weight information of each first-tier primary criteria 
    """
    yaml_file_path = f'./other_resources/scenario_criteria/specials/{category.strip()}.yaml'
    with open(yaml_file_path, 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        
    # parse the criteria
    criteria_ = ['# List of Criteria']
    for key, value in data.items():
        for criteria_name, criteria in value.items():
            if criteria['weight'] <= 2:
                # 1, 2
                degree = 'normal'
            elif 2 < criteria['weight'] <= 4:
                # 3, 4
                degree = 'medium'
            else:
                degree = 'important'
            if with_degree is False:
                criteria_.append(f'## {criteria_name}\nDescription: {criteria["content"]}\n\n')
            else:
                criteria_.append(f'## {criteria_name}\nDescription: {criteria["content"]}\nDegree: {degree}\n\n')
    criteria = '\n'.join(criteria_[:max_num])
    return criteria



def load_test_data(domain='translate', use_classifier=False, max_num=100):
    path = f'filter_data/ranked_data/{domain}_feedback_correction.json'
    with open(path) as f:
        test_data = json.load(f)

    test_data_list = []
    dataset = load_dataset("lmsys/chatbot_arena_conversations")
    counter = 0
    for item in tqdm(dataset['train']):
        winner = item['winner']
        if winner == 'model_a':
            conversation = item['conversation_a']
        else:
            conversation = item['conversation_b']
        if len(conversation) != 2:
            continue
        input = conversation[0]['content']
        response = conversation[1]['content']
        
        if use_classifier is True:
            criteria_type, _ = classifier.chat(input)
            try:
                criteria_raw = read_yaml(criteria_type)
            except:
                criteria_raw = ''
            
        test_data_list.append({
            "task_description": "answer user's question",
            "input": input,
            "response": segment_response(response),
            "my_criteria": criteria_raw
        })
        counter += 1
        if counter == max_num:
            break
    return test_data_list


def load_test_data_v2(
    datasets={},
    read_path='filter_data/ranked_data', 
    dataset_name='autoj_dataset.json', 
    key_name='code_generation', 
    sample_index=0, 
    save_path='',
    error_files=set()
):
    '''对dataset中key类型的数据，从start_index开始，执行number个样本数据'''
    item = datasets[dataset_name][key_name][sample_index]
    responses = {}
    response_names = {}
    criteria_types = []
    for index_j, res in enumerate(item['responses']):
        if index_j == 0:
            quality = 'low'
        elif index_j == 1:
            quality = 'medium'
        else:
            quality = 'high'
        criteria_type = res['response']['task']
        # for openhermes, the coding_generation and airoboro2.2_orca should be covered, where the task is None
        if criteria_type is None or criteria_type == '':
            criteria_type = key_name
        
        criteria_types.append(criteria_type)
        try:
            criteria_raw = read_yaml(criteria_type)
        except:
            criteria_raw = ''
        response = segment_response(
            res['response']['content'],
            criteria_type=criteria_type
        )
        responses[quality] = response
        response_names[quality] = res['llm_name']
    assert len(set(criteria_types)) == 1
    sample = {
        "input": item['conversation_history'],
        "responses": responses,
        "my_criteria": criteria_raw,
        "criteria_type": criteria_type,
        "dataset": dataset_name,
        "key_name": key_name,
        "index": sample_index,
        "response_llm_names": response_names,
        "save_path": save_path,
        "read_path": read_path,
        "raw_data": item,
        "file_names": {
            q: os.path.join(
                save_path, 
                f"DatasetName_{dataset_name.replace('.json', '')}_KeyName_{key_name}_SampleIndex_{sample_index}_Quality_{q}.json"
            ) for q in responses
        }
    }
    for q, file_name in sample['file_names'].items():
        if os.path.exists(file_name) is False:
            return sample
        else:
            # or the sample is error
            _, filename = os.path.split(file_name)
            if filename in error_files:
                print(f'[!] found the error file, append it into the task queue:', filename)
                return sample
            with open(file_name) as f:
                dd = json.load(f)
            if dd['status'] == 'ERROR':
                return sample

    # print(file_name)
    return None

    
def compute_and_save_price(prices_openai, item):
    t_ctx, t_gen = item['t_ctx'], item['t_gen']
    prices = {
        "prompt_tokens": [],
        "prompt_prices": [],
        "completion_tokens": [],
        "completion_prices": []
    }
    for t_ctx_, t_gen_ in zip(t_ctx, t_gen):
        price_1 = t_ctx_ * prices_openai['prompt']
        price_2 = t_gen_ * prices_openai['completion']
        prices['prompt_tokens'].append(t_ctx_)
        prices['completion_tokens'].append(t_gen_)
        prices['prompt_prices'].append(price_1)
        prices['completion_prices'].append(price_2)
    prices['overall_price'] = sum(prices['prompt_prices']) + sum(prices['completion_prices'])
    item['prices'] = prices


# 只有high-quality和low-quality. 针对metamath数据集，high-quality是正确样本，low-quality是错误样本。针对codefeedback数据集，high-quailty是数据集原本gpt-3.5-turbo生成的结果，low-quality是5个低质量语言模型生成的结果
def load_test_data_v3(
    datasets={},
    read_path='filter_data/ranked_data', 
    dataset_name='metamathqa_dataset.json', 
    key_name='code_generation', 
    sample_index=0, 
    save_path='',
    error_files=set()
):
    '''对dataset中key类型的数据，从start_index开始，执行number个样本数据'''
    item = datasets[dataset_name][key_name][sample_index]
    responses = {}
    response_names = {}
    criteria_types = []
    assert len(item['responses']) == 2
    for index_j, res in enumerate(item['responses']):
        if index_j == 0:
            quality = 'low'
        else:
            quality = 'high'
        criteria_type = res['response']['task']
        # for openhermes, the coding_generation and airoboro2.2_orca should be covered, where the task is None
        if criteria_type is None or criteria_type == '':
            criteria_type = key_name
        
        criteria_types.append(criteria_type)
        try:
            criteria_raw = read_yaml(criteria_type)
        except:
            criteria_raw = ''
        response = segment_response(
            res['response']['content'],
            criteria_type=criteria_type
        )
        responses[quality] = response
        response_names[quality] = res['llm_name']
    assert len(set(criteria_types)) == 1
    sample = {
        "input": item['conversation_history'],
        "responses": responses,
        "my_criteria": criteria_raw,
        "criteria_type": criteria_type,
        "dataset": dataset_name,
        "key_name": key_name,
        "index": sample_index,
        "response_llm_names": response_names,
        "save_path": save_path,
        "read_path": read_path,
        "raw_data": item,
        "file_names": {
            q: os.path.join(
                save_path, 
                f"DatasetName_{dataset_name.replace('.json', '')}_KeyName_{key_name}_SampleIndex_{sample_index}_Quality_{q}.json"
            ) for q in responses
        }
    }
    for q, file_name in sample['file_names'].items():
        if os.path.exists(file_name) is False:
            return sample
        else:
            # or the sample is error
            _, filename = os.path.split(file_name)
            if filename in error_files:
                print(f'[!] found the error file, append it into the task queue:', filename)
                return sample
            with open(file_name) as f:
                dd = json.load(f)
            if dd['status'] == 'ERROR':
                return sample

    print(file_name)
    return None



def load_test_data_v3_stage_2(
    read_path='filter_data/ranked_data', 
    dataset_name='metamathqa_dataset.json', 
    key_name='code_generation', 
    sample_index=0, 
    save_path='',
    error_files=set()
):
    for dataset_name in os.listdir(read_path):
        for task_name in os.listdir(os.path.join(read_path, dataset_name)):
            folder_path = os.path.join(read_path, dataset_name, task_name)
            for file in os.listdor(folder_path):
                item = json.load(open(file))
                sample = {
                    "input": item['conversation_history'],
                    "responses": responses,
                    "my_criteria": criteria_raw,
                    "criteria_type": criteria_type,
                    "dataset": dataset_name,
                    "key_name": key_name,
                    "index": sample_index,
                    "response_llm_names": response_names,
                    "save_path": save_path,
                    "read_path": read_path,
                    "raw_data": item,
                    "file_names": {
                        q: os.path.join(
                            save_path, 
                            f"DatasetName_{dataset_name.replace('.json', '')}_KeyName_{key_name}_SampleIndex_{sample_index}_Quality_{q}.json"
                        ) for q in responses
                    }
                }


    '''对dataset中key类型的数据，从start_index开始，执行number个样本数据'''
    item = datasets[dataset_name][key_name][sample_index]
    responses = {}
    response_names = {}
    criteria_types = []
    assert len(item['responses']) == 2
    for index_j, res in enumerate(item['responses']):
        if index_j == 0:
            quality = 'low'
        else:
            quality = 'high'
        criteria_type = res['response']['task']
        # for openhermes, the coding_generation and airoboro2.2_orca should be covered, where the task is None
        if criteria_type is None or criteria_type == '':
            criteria_type = key_name
        
        criteria_types.append(criteria_type)
        try:
            criteria_raw = read_yaml(criteria_type)
        except:
            criteria_raw = ''
        response = segment_response(
            res['response']['content'],
            criteria_type=criteria_type
        )
        responses[quality] = response
        response_names[quality] = res['llm_name']
    assert len(set(criteria_types)) == 1
    sample = {
        "input": item['conversation_history'],
        "responses": responses,
        "my_criteria": criteria_raw,
        "criteria_type": criteria_type,
        "dataset": dataset_name,
        "key_name": key_name,
        "index": sample_index,
        "response_llm_names": response_names,
        "save_path": save_path,
        "read_path": read_path,
        "raw_data": item,
        "file_names": {
            q: os.path.join(
                save_path, 
                f"DatasetName_{dataset_name.replace('.json', '')}_KeyName_{key_name}_SampleIndex_{sample_index}_Quality_{q}.json"
            ) for q in responses
        }
    }
    for q, file_name in sample['file_names'].items():
        if os.path.exists(file_name) is False:
            return sample
        else:
            # or the sample is error
            _, filename = os.path.split(file_name)
            if filename in error_files:
                print(f'[!] found the error file, append it into the task queue:', filename)
                return sample
            with open(file_name) as f:
                dd = json.load(f)
            if dd['status'] == 'ERROR':
                return sample

    print(file_name)
    return None



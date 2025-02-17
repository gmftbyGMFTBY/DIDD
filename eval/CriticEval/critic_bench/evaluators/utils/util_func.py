import re
try:
    from .exec import *
except:
    pass


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
        if not response.strip():
            response = 'Empty Response'
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


def autoj_parse_score_func(string):
    rest = re.findall('\[\[(\d+)\]\]', string)
    try:
        return float(rest[0])
    except:
        return None


def ultracm_parse_score_func(string):
    if string[0].isnumeric():
        return float(string[0])
    else:
        return None


def tigerscore_parse_score_func(string):
    try:
        item = json.loads(string)
        rest_string = item['raw_output']
        rest = re.findall('Score reduction \d: (\d+)', rest_string)
        rest = sum([-float(r) for r in rest])
        return rest
    except:
        rest = re.findall('Score reduction \d: (\d+)', string)
        rest = sum([-float(r) for r in rest])
        return rest
    

def extract_score(string):
    try:
        try:
            decision = re.findall('.*(Score: .+)', string)[0].replace('Score:', '').replace('\\n', '').strip()
            decision = float(decision)
        except:
            try:
                decision = float(decision.split()[0])
            except:
                decision = parse_math_result(string)
    except:
        decision = None
    return decision


def extract_decision_float(string):
    try:
        try:
            decision = re.findall('Score: (\d+\.\d+|\d+)', string)
            decision = float(decision[0])
        except Exception as error:
            try:
                decision = float(decision.split()[0])
            except:
                decision = parse_math_result(string)
    except:
        decision = None
    return decision




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


def extract_decision_option_label(string):
    try:
        decision = re.findall('.*(Label: .+)', string)[0].replace('Label:', '').strip()
    except:
        decision = string.replace('.', '').strip()
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

def parse_math_result(string):
    '''最终答案肯定在后面，我们从后面parse数字即可'''
    try:
        if type(string) == dict:
            if 'Rationale' in string:
                string = string['Rationale']
            elif 'rationale' in string:
                string = string['rationale']
            elif 'Answer' in string:
                string = ' ' + string['Answer'] + ' '
            else:
                ipdb.set_trace()
        elif type(string) in [int, float]:
            return string
        string = string.replace('\n', ' ').replace('=', '= ').replace('.', ' ').replace(',', '')
        #string = string.replace('\n', ' ').replace('=', '= ').replace(',', ' ')
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


def parse_code(code, lang='python'):
    pattern = rf'```{lang}.*?\s+(.*?)```'
    match = re.search(pattern, code, re.DOTALL)
    if match:
        code_ = match.group(1)
    else:
        # print(f'do not match any code from: {code}')
        if '```python' not in code and '```' not in code:


            return code
        else:
            return ''
    return code_

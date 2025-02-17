import json
from itertools import chain
from copy import deepcopy
import re
import random
from tqdm import tqdm
import os
from collections import Counter
import ipdb


"""效仿 autoj 测试不同的领域数据对模型 critique 能力的影响

1. summarization
2. exam question
3. rewriting
4. code
5. creative writing
6. functional writing
7. general communication
8. nlp tasks
"""



def remove_labels(string):
    new_string = re.sub(r'\[S\d+\]', '', string)
    return new_string

def convert(item):
    conversation_input = '\n'.join([f'["Begin of Utterance"] {utterance["role"]}: {utterance["content"]} [End of Utterance]' for utterance in item['input'] + [{'role': 'assistant', 'content': item['response']}]])
    conversation = [{'input': conversation_input, 'output': item['critique'][-1]}]
    return conversation


def mapping_to_domain(string, item):
    string = string.lower()

    mappings = {
        'summarization': set(['post_summarization', 'text_summarization', 'note_summarization', 'airoboro2.2_summarization']),
        'exam_question': set(['math_reasoning', 'exam_question_with_math', 'exam_question_without_math', 'solving_exam_question_without_math', 'solving_exam_question_with_math', 'airoboro2.2_cot', 'camelai_physical', 'airoboro2.2_quiz', 'camelai_chemistry', 'MetaMathQA_GSM_AnsAug', 'MetaMathQA_MATH_Rephrased', 'airoboro2.2_multiple_choice']),
        'rewriting': set(['text_simplification', 'language_polishing', 'instructional_rewriting', 'text_correction', 'paraphrasing', 'airoboro2.2_editor']),
        'code': set(['code_simplification', 'code_generation', 'explaining_code', 'code_correction_rewriting', 'code_to_code_translation', 'airoboro2.2_coding', 'CodeFeedback_code_generation']),
        'creative_writing': set(['writing_song_lyrics', 'writing_social_media_post', 'general_creative_writing', 'counterfactual', 'writing_personal_essay', 'writing_blog_post', 'writing_advertisement', 'writing_marketing_materials', 'writing_presentation_script', 'creative_writing', 'airoboro2.2_counterfactual_contextual', 'airoboro2.2_writing', 'airoboro2.2_song', 'airoboro2.2_detailed_writing']),
        'functional_writing': set(['writing_product_description', 'writing_news_article', 'writing_biography', 'writing_legal_document', 'writing_technical_document', 'writing_job_application', 'writing_scientific_paper', 'general_functional_writing', 'writing_cooking_recipe', 'writing_email', 'functional_writing', 'airoboro2.2_stylized_response', 'airoboro2.2_plan']),
        'general_communication': set(['asking_how_to_question', 'seeking_advice', 'verifying_fact', 'open_question', 'analyzing_general', 'explaining_general', 'brainstorming', 'roleplay', 'planning', 'chitchat', 'recommendation', 'value_judgment', 'rejecting', 'value_judgement', 'airoboro2.2_joke']),
        'nlp_tasks': set(['ranking', 'text_to_text_translation', 'data_analysis', 'classification_identification', 'title_generation', 'question_generation', 'reading_comprehension', 'keywords_extraction', 'information_extraction', 'topic_modeling'])
    }

    for key, value in mappings.items():
        if string in value:
            return key
    #if string in ['default', 'ultrachat', 'sharegpt', 'oasst2', 'airoboro2.2_awareness', 'airoboro2.2_misconception', 'airoboro2.2_general', 'airoboro2.2_experience', 'airoboro2.2_theory_of_mind']:
    #    return None
    #ipdb.set_trace()
    return None


if __name__ == "__main__":
    random.seed(0)
    prompt = open('prompts/singlewise_critique.md').read()

    file = '../multicritique_sft/train.jsonl'

    pbar = tqdm(total=64804)
    new_data = {}
    masked_category = []
    with open(file) as f:
        for line in f:
            item = json.loads(line)
            category = mapping_to_domain(item['key_name'], item)
            if category is None:
                masked_category.append(item['key_name'])
                pbar.update(1)
                continue
            if category not in new_data:
                new_data[category] = []
            quality = item['evaluated_response_quality']
            ipt = item['input']
            response = item['responses'][quality]
            critique = item['parse_final_feedbacks']
            score = item['parse_final_judgement_score']
            new_data[category].append({
                'input': ipt,
                'response': response,
                'critique': critique,
                'score': score
            })
            pbar.update(1)

    #print(Counter(masked_category).most_common())
    #ipdb.set_trace()

    datasets = []
    max_base_num = 3000
    for key in new_data:
        data = []
        for sample in new_data[key]:
            conv = '[begin of conversation] ' + '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in sample['input']]) + ' [end of conversation]'
            string = prompt.format(conversation=conv, response=remove_labels(response))
            data.append({'conversation': [{'input': string, 'output': sample['critique'][-1]}]})
        datasets.append(data)
        with open(f'data/analysis_{key}.json', 'w') as f:
            dd = random.sample(data, min(max_base_num, len(data)))
            json.dump(dd, f, ensure_ascii=False, indent=4)
        print(f'[!] {key}:', len(dd))

    max_length = max([len(data) for data in datasets]) // len(new_data) + 10
    overall = []
    for data in datasets:
        overall.extend(random.sample(data, min(max_length, len(data))))
    with open(f'data/analysis_overall.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f'[!] overall:', len(overall))

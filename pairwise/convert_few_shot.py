import json
from tqdm import tqdm
import os
import re
import ipdb



def collect_train_set():
    trainset = {}
    for file in os.listdir('output'):
        path = os.path.join('output', file)
        d = json.load(open(path))
        input = d['conv'][0]['content']
        query = re.findall('# 1. 用户 query 或对话历史(.+)### 2. 生成内容 A', input, re.DOTALL | re.MULTILINE)
        responsea = re.findall('# 2. 生成内容 A(.+)### 2. 生成内容 B', input, re.DOTALL | re.MULTILINE)
        responseb = re.findall('# 2. 生成内容 B(.+)# 你的输出格式', input, re.DOTALL | re.MULTILINE)
        assert len(responsea) == len(responseb) == len(query)
        responsea = responsea[0].strip()
        responseb = responseb[0].strip()
        query = query[0].strip().replace('[begin of conversation]', '').replace('[end of conversation]', '')
        trainset[query] = d['conv'][1]['content']
    return trainset


def collect_few_shots():
    file = '../multicritique_sft/train.jsonl'
    pbar = tqdm(total=64804)
    new_data = {}
    with open(file) as f:
        for line in f:
            item = json.loads(line)
            string = '\n'.join([f'{utterance["role"]}: {utterance["content"]}' for utterance in item['input']])

            domain = None
            for key, value in mappings.items():
                if item['key_name'] in value:
                    domain = key
                    break
            if domain:
                if domain not in new_data:
                    new_data[domain] = {}
                quality = item['evaluated_response_quality']
                ipt = item['input']
                response = item['responses'][quality]
                score = item['parse_final_judgement_score']
                new_data[domain][quality] = {
                    'input': ipt,
                    'response': response,
                    'score': score,
                    'string': string
                }
                pbar.update(1)
            else:
                pbar.update(1)
    return new_data


if __name__ == "__main__":
    trainset = collect_train_set()
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


    few_shot = collect_few_shots()
    new_few_shot = {}
    for domain, sample in few_shot.items():
        if domain not in new_few_shot:
            new_few_shot[domain] = {}
        if len(sample) == 2:
            q1, q2 = list(sample.keys())
            string = sample[q1]['string']
            if string in trainset:
                critique = trainset[string]
            else:
                continue
            if set([q1, q2]) == set(['low', 'high']):
                label = 'low-high'
            elif set([q1, q2]) == set(['low', 'medium']):
                label = 'low-medium'
            elif set([q1, q2]) == set(['high', 'medium']):
                label = 'medium-high'
            if label not in new_few_shot:
                new_few_shot[domain][label] = []
            new_few_shot[domain][label].append({
                'input': sample[q1]['input'],
                'responsea': sample[q1]['response'],
                'responseb': sample[q2]['response'],
                'critique': critique
            })
        elif len(sample) == 3:
            qualities = ['low', 'medium', 'high']
            string = sample['low']['string']
            if string in trainset:
                critique = trainset[string]
            else:
                continue
            for q1 in ['low', 'medium']:
                for q2 in ['medium', 'high']:
                    if q1 == q2:
                        continue
                    label = f'{q1}-{q2}'
                    if label not in new_few_shot:
                        new_few_shot[domain][label] = []
                    new_few_shot[domain][label].append({
                        'input': sample[q1]['input'],
                        'responsea': sample[q1]['response'],
                        'responseb': sample[q2]['response'],
                        'critique': critique,
                    })

    for domain, value in new_few_shot.items():
        #assert len(value) > 0
        for quality, v in value.items():
            assert len(v) > 0 


    with open('new_few_shot.json', 'w') as f:
        json.dump(new_few_shot, f, ensure_ascii=False, indent=4)

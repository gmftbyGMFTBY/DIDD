import json
import ipdb

if __name__ == "__main__":
    few_shot = json.load(open('few_shot.json'))
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
    new_few_shot = {key: {} for key in mappings}
    for key in few_shot:
        #
        key_ = None
        for k, v in mappings.items():
            if key in v:
                key_ = k
                break
        if key_:
            for quality in few_shot[key]:
                if quality not in new_few_shot[key_]:
                    new_few_shot[key_][quality] = []
                new_few_shot[key_][quality].extend(few_shot[key][quality])

    with open('new_few_shot.json', 'w') as f:
        json.dump(new_few_shot, f, ensure_ascii=False, indent=4)



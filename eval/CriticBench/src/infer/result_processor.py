import multiprocess
import numpy as np
import json
import ipdb
import re
from sklearn.metrics import f1_score, accuracy_score, recall_score
from collections import defaultdict

import evaluate_configuration
from utils.parser import extract_answer_str_by_answer_pattern, extract_answer_by_question_source
from utils.grader import EM, math_equal
from utils.code_eval.code_eval import compute_code_eval

class ResultProcessor:
    def result_check(self, task, dataset_with_prompt, result_list, enable_code_execution):
        result_by_id = {sample["id"]: sample for sample in result_list}
        for sample in dataset_with_prompt:
            q_id = sample["id"]
            question = sample["question"]
            if task in ["generation", "correction"]:
                golden_answers = sample["answer"]
            elif task in ["critique"]:
                golden_answer = sample["response_label"]
            dataset_name = sample["question_source"]
            if q_id in result_by_id:
                pred_str = result_by_id[q_id][f"{task}_result"]
                answer_pattern = sample["prompt_info_dict"]["answer_pattern"]
                answer_str = extract_answer_str_by_answer_pattern(pred_str=pred_str, answer_pattern=answer_pattern)
                clean_pred = extract_answer_by_question_source(pred_str=answer_str, question_source=dataset_name, task=task)
                #if 'improved solution"' in pred_str.lower():
                #    print(f'[!] ERROR')
                #    #ipdb.set_trace()
                if task in ["generation", "correction"]:
                    label = False
                    if dataset_name in ["HotpotQA", "AmbigNQ"]:
                        for g in golden_answers:
                            if EM(clean_pred, g):
                                label = True
                    elif dataset_name in ["AQuA", "Colored Object", "CSQA", "Date", "Penguins"]:  # 选择题
                        for g in golden_answers:
                            if math_equal(g.lower(), clean_pred.lower()):
                                label = True
                    elif dataset_name == "HumanEval":
                        if "def" not in pred_str:
                            pred_str = question + pred_str
                        if task == "correction":
                            result_by_id[q_id][f"{task}_result"] = ((pred_str).replace("[DONE]", "")
                                                                    .replace("[BEGIN]", "")
                                                                    .replace("```python", "")
                                                                    .replace("```", ""))
                        else:
                            result_by_id[q_id][f"{task}_result"] = pred_str
                        label = False
                    elif dataset_name == "MBPP":
                        result_by_id[q_id][f"{task}_result"] = pred_str.replace("[DONE]", "").replace("[BEGIN]", "")
                        label = False
                    elif dataset_name == "Repeat Copy":
                        result_by_id[q_id][f"{task}_result"] = pred_str.strip()
                        clean_pred = pred_str.strip()
                        #clean_pred = clean_pred.replace('{"answer":"', '').replace('"}', '')
                        #clean_pred = clean_pred.replace('.', '').replace(',', '')

                        for g in golden_answers:
                            if math_equal(clean_pred, g):
                                label = True
                    else:  # GSM8K, MATH, Object Counting, StrategyQA, TabMWP
                        for g in golden_answers:
                            if isinstance(g, str):
                                g = g.lower()
                            if isinstance(clean_pred, str):
                                clean_pred = clean_pred.lower()
                            if math_equal(clean_pred, g):
                                label = True
                    result_by_id[q_id][f"{task}_check"] = label
                elif task in ["critique"]:
                    result_by_id[q_id][f"{task}_check"] = [golden_answer, clean_pred]
            else:
                result_by_id[q_id] = {"id":q_id, f"{task}_result": "", f"{task}_check": False}
        if enable_code_execution and task in ["generation", "correction"]:
            result_by_id = self.check_code(task=task, dataset_with_prompt=dataset_with_prompt, result_by_id=result_by_id)
        return result_by_id

    def critic_model_result_check(self, model, task, dataset, result_list):
        result_by_id = {sample["id"]: sample for sample in result_list}
        error_num = 0
        scores_ = []
        for sample in dataset:
            q_id = sample["id"]
            golden_answer = sample["response_label"]
            if q_id in result_by_id:
                pred_str = result_by_id[q_id][f"{task}_result"]
                clean_pred = None
                if 1:
                    #if 'True' in pred_str:
                    #    clean_pred = False
                    #else:
                    #    clean_pred = True
                    #'''
                    try:
                        scores = re.findall('Score: (\d+.\d+)', pred_str)
                        score = float(scores[-1])
                        scores_.append(score)
                        if score >= 2.5:
                            clean_pred = True
                        else:
                            clean_pred = False
                    except Exception as error:
                        try:
                            scores = re.findall('Score: (\d+)', pred_str)
                            score = float(scores[-1])
                            scores_.append(score)
                            if score >= 2.5:
                                clean_pred = True
                            else:
                                clean_pred = False
                        except:
                            clean_pred = not golden_answer
                    #'''
                elif ("incorrect" in pred_str or "wrong" in pred_str or "incomplete" in pred_str or "not helpful" in pred_str or
                        "error" in pred_str):
                    clean_pred = False
                elif "correct" in pred_str or "accurate" in pred_str or "good" in pred_str or "concise" in pred_str:
                    clean_pred = True

                if clean_pred is None:
                    clean_pred = not golden_answer
                result_by_id[q_id][f"{task}_check"] = [golden_answer, clean_pred]
            else:
                result_by_id[q_id] = {"id":q_id, f"{task}_result": "", f"{task}_check": False}
                
        #ipdb.set_trace()
        #from collections import Counter
        #print(Counter(scores_).most_common())

        print('[!] Error Num:', error_num)
        return result_by_id

    def check_code(self, task, dataset_with_prompt, result_by_id):
        predictions = []
        references = []
        for sample in dataset_with_prompt:
            q_id = sample["id"]
            golden_answer = sample["answer"]
            if sample["prompt_info_dict"]["answer_pattern"] in ["code", "json: code"]:
                final_code = result_by_id[q_id][f"{task}_result"]
                predictions.append([q_id, final_code])
                references.append(golden_answer[0])
        num_worker = multiprocess.cpu_count()
        results, detailed_result = compute_code_eval(predictions=predictions,
                          references=references,
                          num_workers=num_worker)
        for q_id in detailed_result:
            result_by_id[q_id][f"{task}_check"] = detailed_result[q_id][0][1]["passed"]

        return result_by_id

    def analyse_result(self, task, dataset_with_prompt, result_by_id):
        check_by_type = defaultdict(list)
        check_by_dataset = defaultdict(list)
        total_check = []
        acc_pos_score_by_type = defaultdict(float)
        acc_neg_score_by_type = defaultdict(float)
        acc_score_by_type = defaultdict(float)
        acc_pos_score_by_dataset = defaultdict(float)
        acc_neg_score_by_dataset = defaultdict(float)
        acc_score_by_dataset = defaultdict(float)
        total_score = 0.0
        for sample in dataset_with_prompt:
            q_id = sample["id"]
            dataset_name = sample["question_source"]
            question_type = sample["question_type"]
            if q_id in result_by_id:
                check = result_by_id[q_id][f"{task}_check"]
                check_by_type[question_type].append(check)
                check_by_dataset[dataset_name].append(check)
                total_check.append(check)
        if task in ["generation", "correction"]:
            for type in check_by_type:
                score_by_type[type] = 100 * sum(check_by_type[type]) / len(check_by_type[type])
            for dataset in check_by_dataset:
                score_by_dataset[dataset] = 100 * sum(check_by_dataset[dataset]) / len(check_by_dataset[dataset])
            total_score = 100 * sum(total_check) / len(total_check)
        elif task in ["critique"]:  # F1 score of wrong label
            for type in check_by_type:
                # acc positive
                pred_labels = []
                for check in check_by_type[type]:
                    if check[0] is True:
                        if check == "" or check[1] == "":
                            pred_labels.append(0)
                        else:
                            pred_labels.append(int(check[1] == check[0]))
                acc_pos_score_by_type[type] = 100 * np.mean(pred_labels)
                # acc negative
                pred_labels = []
                for check in check_by_type[type]:
                    if check[0] is False:
                        if check == "" or check[1] == "":
                            pred_labels.append(0)
                        else:
                            pred_labels.append(int(check[1] == check[0]))
                acc_neg_score_by_type[type] = 100 * np.mean(pred_labels)
                acc_score_by_type[type] = 2 * acc_pos_score_by_type[type] * acc_neg_score_by_type[type] / (acc_pos_score_by_type[type] + acc_neg_score_by_type[type])
            for dataset in check_by_dataset:
                # acc positive
                pred_labels = []
                for check in check_by_dataset[dataset]:
                    if check[0] is True:
                        if check == "" or check[1] == "":
                            pred_labels.append(0)
                        else:
                            pred_labels.append(int(check[1] == check[0]))
                acc_pos_score_by_dataset[dataset] = 100 * np.mean(pred_labels)
                # acc negative
                pred_labels = []
                for check in check_by_dataset[dataset]:
                    if check[0] is False:
                        if check == "" or check[1] == "":
                            pred_labels.append(0)
                        else:
                            pred_labels.append(int(check[1] == check[0]))
                acc_neg_score_by_dataset[dataset] = 100 * np.mean(pred_labels)
                acc_score_by_dataset[dataset] = 2 * acc_pos_score_by_dataset[dataset] * acc_neg_score_by_dataset[dataset] / (acc_pos_score_by_dataset[dataset] + acc_neg_score_by_dataset[dataset])
            # acc positive
            pred_labels = []
            for check in total_check:
                if check[0] is True:
                    if check == "" or check[1] == "":
                        pred_labels.append(0)
                    else:
                        pred_labels.append(int(check[1] == check[0]))
            acc_pos_score = 100 * np.mean(pred_labels)
            # acc positive
            pred_labels = []
            for check in total_check:
                if check[0] is False:
                    if check == "" or check[1] == "":
                        pred_labels.append(0)
                    else:
                        pred_labels.append(int(check[1] == check[0]))
            acc_neg_score = 100 * np.mean(pred_labels)
            total_score = 2 * acc_pos_score * acc_neg_score / (acc_pos_score + acc_neg_score)
        return total_score, acc_score_by_type, acc_score_by_dataset


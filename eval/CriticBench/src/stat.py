import json
import re
import ipdb
from tqdm import tqdm
from collections import Counter
import numpy as np


def parse_score(pred_str):
    patterns = ['Score: (\d+.\d+)', 'Score: (\d+)']
    for pattern in patterns:
        try:
            scores = re.findall(pattern, pred_str)
            score = float(scores[-1])
            return score
        except:
            pass
    return None

if __name__ == "__main__":
    pathes = [
        'train_v1/_home_lt_NewPoNe_train_work_dirs_llama3_8b_instruct_qlora_alpaca_e3_copy_iter_2658_merged_hf/critique/result_12_26_00_27_04.jsonl',
        'train_v2/_home_lt_NewPoNe_train_work_dirs_llama3_8b_instruct_qlora_alpaca_e3_train_v2_iter_1725_merge_hf/critique/result_12_26_14_46_52.jsonl',
        'train_v3/_home_lt_NewPoNe_train_work_dirs_llama3_8b_instruct_qlora_alpaca_e3_train_v3_iter_1848_merge_hf/critique/result_12_26_17_01_24.jsonl'
    ]
    for path in pathes:
        data = [parse_score(json.loads(line)['critique_result']) for line in open(path).readlines()]
        data = [i for i in data if i is not None]
        print('=' * 10, path, '=' * 10)
        print(Counter(data).most_common())
        print(np.mean(data))
        print('=' * 10, path, '=' * 10)


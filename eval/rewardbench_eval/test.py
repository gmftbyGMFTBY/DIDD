from utils import *
import numpy as np
from tabulate import tabulate
import re
from tqdm import tqdm
import json
import os
import sys
import ipdb
import argparse
from datasets import load_from_disk, load_dataset
from constant import *


def calculate_scores_per_section(metrics):
    """
    Helper function for immediately logging RewardBench scores.
    """
    example_counts = EXAMPLE_COUNTS
    subset_mapping = SUBSET_MAPPING
    section_scores = {}
    for section, tests in subset_mapping.items():
        total_weighted_score = 0
        total_examples = 0
        for test in tests:
            if test in metrics:
                total_weighted_score += metrics[test] * example_counts[test]
                total_examples += example_counts[test]
        if total_examples > 0:
            section_scores[section] = total_weighted_score / total_examples
        else:
            section_scores[section] = 0
    return section_scores



def parser_args():
    parser = argparse.ArgumentParser(description='train parameters')
    parser.add_argument('--output_dir', type=str, default='outputs_20240630_resumm_ablation_study')
    return parser.parse_args() 


if __name__ == "__main__":
    args = vars(parser_args())
    dataset = load_dataset("allenai/reward-bench", split="filtered")
    subsets = list(set(dataset['subset'])) + [None]

    results = [['model_name'] + subsets[:-1] + ['All', 'Error']]
    #results_reversed = [['model_name'] + subsets[:-1] + ['All', 'Error']]
    overall_scores = []
    #overall_scores_reversed = []

    for folder in os.listdir(args['output_dir']):

        #if 'reduce_rep' not in folder:
        #    continue

        error_counter = 0
        p, p_reversed = [], []
        p.append(folder)
        #p_reversed.append(folder)

        for subset in subsets:

            #if subset not in  [
            #    'mt-bench-hard',
            #    'llmbar-natural',
            #    'llmbar-adver-neighbor',
            #    'llmbar-adver-GPTInst',
            #    'llmbar-adver-GPTOut',
            #    'llmbar-adver-manual'
            #]:
            #    continue

            folder_path = os.path.join(args['output_dir'], folder)

            try:
                file_path = os.path.join(folder_path, 'response_test')
                data = load_from_disk(file_path)
                if subset is not None:
                    data = data.filter(lambda ex: ex["subset"] == subset)
            except Exception as error:
                print(f'[!] LOAD ERROR:', error)
                continue

            rest, rest_reversed = [], []
            error = 0
            tie_num = 0
            win_num, loss_num = 0, 0
            for index in tqdm(range(len(data))):
                sample = data[index]
                evaluation = sample['evaluate']
                label = re.findall('Label: (A|B)', evaluation)
                assert len(label) >= 1
                label = label[-1]
                if label == 'A':
                    rest.append(1)
                else:
                    rest.append(0)
            p.append(round(np.mean(rest), 4))
            #p_reversed.append(round(1-np.mean(rest_reversed), 4))

        results.append(p)
        #results_reversed.append(p_reversed)
        metrics = {key: value for key, value in zip(results[0][1:-2], results[-1][1:-2])}

        #metrics_reversed = {key: value for key, value in zip(results_reversed[0][1:-2], results_reversed[-1][1:-2])}

        scores = calculate_scores_per_section(metrics)
        scores['Overall'] = np.mean(list(scores.values()))
        #scores_reversed = calculate_scores_per_section(metrics_reversed)
        #scores_reversed['Overall'] = np.mean(list(scores_reversed.values()))
        scores['Error'] = error_counter
        #scores_reversed['Error'] = error_counter
        overall_scores.append(scores)
        #overall_scores_reversed.append(scores_reversed)

    final_rest = [['Model'] + list(overall_scores[0].keys())]
    assert len(overall_scores) == len(results) - 1
    for item, aa in zip(overall_scores, results[1:]):
        final_rest.append([aa[0]])
        for key in final_rest[0][1:]:
            final_rest[-1].append(item[key])
        final_rest[-1].append(item['Overall'])
    print(tabulate(final_rest, tablefmt='simple'))

    #final_rest = [['Model'] + list(overall_scores_reversed[0].keys())]
    #assert len(overall_scores_reversed) == len(results_reversed) - 1
    #for item, aa in zip(overall_scores_reversed, results_reversed[1:]):
    #    final_rest.append([aa[0]])
    #    for key in final_rest[0][1:]:
    #        final_rest[-1].append(item[key])
    #    final_rest[-1].append(item['Overall'])
    #print(tabulate(final_rest, tablefmt='simple'))

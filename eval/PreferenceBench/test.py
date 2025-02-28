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


def parser_args():
    parser = argparse.ArgumentParser(description='train parameters')
    parser.add_argument('--output_dir', type=str, default='outputs')
    return parser.parse_args() 


if __name__ == "__main__":
    args = vars(parser_args())
    overall_scores = []

    for folder in os.listdir(args['output_dir']):
        error_counter = 0
        folder_path = os.path.join(args['output_dir'], folder)
        try:
            file_path = os.path.join(folder_path, 'response_test')
            data = load_from_disk(file_path)
        except Exception as error:
            print(f'[!] LOAD ERROR:', error)
            continue
        rest = []
        for index in tqdm(range(len(data))):
            sample = data[index]
            evaluation = sample['evaluate']
            gold = sample['orig_preference']
            label = re.findall('Label: (A|B)', evaluation)
            try:
                assert len(label) >= 1
                label = label[-1]
                if label == gold:
                    rest.append(1)
                else:
                    rest.append(0)
            except:
                error_counter += 1
                rest.append(0)
        print(f'[!] {folder} error counter: {error_counter}; acc:', np.mean(rest))

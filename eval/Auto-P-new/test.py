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
    parser.add_argument('--output_dir', type=str, default='revision_outputs_3b')
    return parser.parse_args() 


if __name__ == "__main__":
    args = vars(parser_args())

    for model in os.listdir(args['output_dir']):
        file_path = os.path.join(args['output_dir'], model, 'result.json')
        if os.path.exists(file_path) is False:
            continue
        with open(file_path) as f:
            data = json.load(f)
        predictions = []
        parsing_error = 0
        for sample in tqdm(data):
            label = sample['label']
            if label == 2:
                continue
            rest = sample['evaluate']
            rest = re.findall('Label: (A|B)', rest)
            try:    
                assert len(rest) >= 1
                rest = rest[-1]
                if rest == 'A':
                    predict = 0
                else:
                    predict = 1
            except:
                predict = 2
            if predict == label:
                predictions.append(1)
            else:
                predictions.append(0)
        print(f'[PARSING ERROR {parsing_error}] {file_path}:', round(np.mean(predictions), 4))


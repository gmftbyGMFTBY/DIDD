#!/bin/bash

echo "[!] hyper-parameters for mode test_set_construction:"
echo "[!] root-path $1"
echo "[!] iter-num: $2"
echo "[!] gen-num: $3"
echo "[!] few-shot-num: $4"
echo "[!] test-query-num: $5"

# save test set into: {root_path}/iter_{iter_num}/test_set_gn_{gen_num}_fsn_{few_shot_num}
python data_generation_iter_exp_v2.py \
    --mode test_set_construction \
    --root-path $1 \
    --iter-num $2 \
    --gen-num $3 \
    --few-shot-num $4 \
    --test-query-num $5 \
    --bsz 8

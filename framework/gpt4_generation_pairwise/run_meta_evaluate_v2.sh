#!/bin/bash

echo "[!] hyper-paramete for mode meta_evaluate"
echo "[!] root-path: $1"
echo "[!] iter-num: $2"
echo "[!] gen-num: $3"
echo "[!] few-shot-num: $4"
echo "[!] test-query-num: $5"

python data_generation_iter_exp_v2.py \
    --mode meta_evaluate \
    --root-path $1 \
    --iter-num $2 \
    --gen-num $3 \
    --few-shot-num $4 \
    --model-prediction-name model_prediction \
    --bsz 8

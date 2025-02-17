#!/bin/bash

echo "[!] hyper-parameter for mode train_set_construction"
echo "[!] root-path: $1"
echo "[!] iter-num: $2"
echo "[!] train-num-each: $3"
echo "[!] few-shot-num: $4"
echo "[!] failure-dis-file: $5"
python data_generation.py \
    --mode train_set_construction \
    --root-path $1 \
    --iter-num $2 \
    --train-num-each $3 \
    --few-shot-num $4 \
    --failure-dis-file $5 \
    --bsz 16

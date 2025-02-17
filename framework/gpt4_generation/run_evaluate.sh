#!/bin/bash


root_path=$1
iter_num=$2
gen_num=$3
few_shot_num=$4
model_path=$5
model_bsz=$6

echo "[!] hyper-parameters for mode: evaluate"
echo "[!] root-path: $1"
echo "[!] iter-num: $2"
echo "[!] gen-num: $3"
echo "[!] few-shot-num: $4"
echo "[!] model-path: $5"
echo "[!] model-bsz: $6"
echo "[!] CUDA_VISIBLE_DEVICES: $7"


# generate prediction results in: {root-path}/iter_{iter-num}/model_prediction_reevaluate.json
CUDA_VISIBLE_DEVICES=$7 python data_generation.py \
    --mode evaluate \
    --root-path $1\
    --iter-num $2 \
    --gen-num $3 \
    --few-shot-num $4 \
    --bsz 16 \
    --model-prompt prompts/singlewise_critique.md \
    --model-path $5 \
    --model-prediction-name model_prediction \
    --model-bsz $6

#--model-path /home/lt/ReNewPoNe/framework/save/baseline/iter_5650_merge_hf \

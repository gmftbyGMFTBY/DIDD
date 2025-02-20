#!/bin/bash

CUDA_VISIBLE_DEVICES=1 xtuner convert pth_to_hf \
    scripts/qwen1_5_7b_baseline.py \
    /home/lt/ReNewPoNe/framework/save/qwen1_5_7b_baseline/iter_5678.pth \
    /home/lt/ReNewPoNe/framework/save/qwen1_5_7b_baseline/iter_5678_hf

#/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct \
# /home/lt/NewPoNe/model/internlm2-7b-chat \
CUDA_VISIBLE_DEVICES=1 xtuner convert merge \
    /home/lt/Qwen1.5-7B-Chat \
    /home/lt/ReNewPoNe/framework/save/qwen1_5_7b_baseline/iter_5678_hf \
    /home/lt/ReNewPoNe/framework/save/qwen1_5_7b_baseline/iter_5678_merge_hf \
    --max-shard-size 2GB

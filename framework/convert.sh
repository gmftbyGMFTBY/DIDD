#!/bin/bash

CUDA_VISIBLE_DEVICES=4 xtuner convert pth_to_hf \
    scripts/baseline.py \
    /home/lt/ReNewPoNe/framework/save/baseline_train_num_4000_iter_0/iter_12682.pth \
    /home/lt/ReNewPoNe/framework/save/baseline_train_num_4000_iter_0/iter_12682_hf

# /home/lt/Qwen1.5-7B-Chat \
#/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct \
CUDA_VISIBLE_DEVICES=4 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/framework/save/baseline_train_num_4000_iter_0/iter_12682_hf \
    /home/lt/ReNewPoNe/framework/save/baseline_train_num_4000_iter_0/iter_12682_merge_hf \
    --max-shard-size 2GB

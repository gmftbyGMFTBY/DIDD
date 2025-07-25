#!/bin/bash

CUDA_VISIBLE_DEVICES=0 xtuner convert pth_to_hf \
    scripts/comp_iter_0_train_num_2000_qwen2.5-0.5b.py \
    /home/lt/ReNewPoNe/pairwise/revision_20250715/qwen2_5_3b_baseline/iter_2568.pth \
    /home/lt/ReNewPoNe/pairwise/revision_20250715/qwen2_5_3b_baseline/iter_2568_hf

# /home/lt/Qwen1.5-7B-Chat \
#/home/lt/ReNewPoNe/framework/save/baseline_20250218/iter_9608_merge_hf \
#/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct \
CUDA_VISIBLE_DEVICES=0 xtuner convert merge \
    /home/lt/Qwen/Qwen2.5-3B-Instruct \
    /home/lt/ReNewPoNe/pairwise/revision_20250715/qwen2_5_3b_baseline/iter_2568_hf \
    /home/lt/ReNewPoNe/pairwise/revision_20250715/qwen2_5_3b_baseline/iter_2568_merge_hf \
    --max-shard-size 2GB

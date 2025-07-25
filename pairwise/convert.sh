#!/bin/bash

CUDA_VISIBLE_DEVICES=1 xtuner convert pth_to_hf \
    scripts/qwen2_5_1_5b_baseline.py \
    /home/lt/ReNewPoNe/pairwise/revision_20250715/qwen2_5_1_5b_baseline/iter_2568.pth \
    /home/lt/ReNewPoNe/pairwise/revision_20250715/qwen2_5_1_5b_baseline/iter_2568_hf

#/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct \
CUDA_VISIBLE_DEVICES=1 xtuner convert merge \
    /home/lt/Qwen/Qwen2.5-1.5B-Instruct \
    /home/lt/ReNewPoNe/pairwise/revision_20250715/qwen2_5_1_5b_baseline/iter_2568_hf \
    /home/lt/ReNewPoNe/pairwise/revision_20250715/qwen2_5_1_5b_baseline/iter_2568_merge_hf \
    --max-shard-size 2GB

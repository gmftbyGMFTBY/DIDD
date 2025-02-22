#!/bin/bash

CUDA_VISIBLE_DEVICES=0 xtuner convert pth_to_hf \
    scripts/baseline.py \
    /home/lt/ReNewPoNe/framework/save/comp_baseline_iter_0_v2/iter_10016.pth \
    /home/lt/ReNewPoNe/framework/save/comp_baseline_iter_0_v2/iter_10016_hf

# /home/lt/Qwen1.5-7B-Chat \
#/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct \
#/home/lt/ReNewPoNe/framework/save/baseline_20250218/iter_9608_merge_hf \
CUDA_VISIBLE_DEVICES=0 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/framework/save/comp_baseline_iter_0_v2/iter_10016_hf \
    /home/lt/ReNewPoNe/framework/save/comp_baseline_iter_0_v2/iter_10016_merge_hf \
    --max-shard-size 2GB

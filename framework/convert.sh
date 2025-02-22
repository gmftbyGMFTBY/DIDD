#!/bin/bash

CUDA_VISIBLE_DEVICES=4 xtuner convert pth_to_hf \
    scripts/baseline.py \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_1_only/iter_2806.pth \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_1_only/iter_2806_hf

# /home/lt/Qwen1.5-7B-Chat \
#/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct \
#/home/lt/NewPoNe/model/internlm2-7b-chat \
CUDA_VISIBLE_DEVICES=4 xtuner convert merge \
    /home/lt/ReNewPoNe/framework/save/baseline_20250218/iter_9608_merge_hf \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_1_only/iter_2806_hf \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_1_only/iter_2806_merge_hf \
    --max-shard-size 2GB

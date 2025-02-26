#!/bin/bash

CUDA_VISIBLE_DEVICES=1 xtuner convert pth_to_hf \
    scripts/baseline.py \
    /home/lt/ReNewPoNe/framework/save/data_mixture_rate_06_8508_iter_1/iter_1000.pth \
    /home/lt/ReNewPoNe/framework/save/data_mixture_rate_06_8508_iter_1/iter_1000_hf

# /home/lt/Qwen1.5-7B-Chat \
#/home/lt/ReNewPoNe/framework/save/baseline_20250218/iter_9608_merge_hf \
#/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct \
CUDA_VISIBLE_DEVICES=1 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/framework/save/data_mixture_rate_06_8508_iter_1/iter_1000_hf \
    /home/lt/ReNewPoNe/framework/save/data_mixture_rate_06_8508_iter_1/iter_1000_merge_hf \
    --max-shard-size 2GB

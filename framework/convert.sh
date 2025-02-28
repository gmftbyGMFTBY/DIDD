#!/bin/bash

CUDA_VISIBLE_DEVICES=2 xtuner convert pth_to_hf \
    scripts/baseline.py \
    /home/lt/ReNewPoNe/framework/save/comp_iter_012_v2_only/iter_4708.pth \
    /home/lt/ReNewPoNe/framework/save/comp_iter_012_v2_only/iter_4708_hf

# /home/lt/Qwen1.5-7B-Chat \
#/home/lt/ReNewPoNe/framework/save/baseline_20250218/iter_9608_merge_hf \
#/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct \
CUDA_VISIBLE_DEVICES=2 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/framework/save/comp_iter_012_v2_only/iter_4708_hf \
    /home/lt/ReNewPoNe/framework/save/comp_iter_012_v2_only/iter_4708_merge_hf \
    --max-shard-size 2GB

#!/bin/bash

CUDA_VISIBLE_DEVICES=1 xtuner convert pth_to_hf \
    scripts/hard_1.py \
    /home/lt/ReNewPoNe/pairwise/save/hard2_rate_07/iter_2016.pth \
    /home/lt/ReNewPoNe/pairwise/save/hard2_rate_07/iter_2016_hf

#/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct \
CUDA_VISIBLE_DEVICES=1 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/pairwise/save/hard2_rate_07/iter_2016_hf \
    /home/lt/ReNewPoNe/pairwise/save/hard2_rate_07/iter_2016_merge_hf \
    --max-shard-size 2GB

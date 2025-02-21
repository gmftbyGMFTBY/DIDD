#!/bin/bash

CUDA_VISIBLE_DEVICES=0 xtuner convert pth_to_hf \
    scripts/overall.py \
    /home/lt/ReNewPoNe/pairwise/save/hard_2/iter_2028.pth \
    /home/lt/ReNewPoNe/pairwise/save/hard_2/iter_2028_hf

CUDA_VISIBLE_DEVICES=0 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/pairwise/save/hard_2/iter_2028_hf \
    /home/lt/ReNewPoNe/pairwise/save/hard_2/iter_2028_merge_hf \
    --max-shard-size 2GB

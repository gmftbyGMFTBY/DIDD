#!/bin/bash

CUDA_VISIBLE_DEVICES=3 xtuner convert pth_to_hf \
    scripts/overall.py \
    /home/lt/ReNewPoNe/pairwise/save/overall/iter_5432.pth \
    /home/lt/ReNewPoNe/pairwise/save/overall/iter_5432_hf

CUDA_VISIBLE_DEVICES=3 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/pairwise/save/overall/iter_5432_hf \
    /home/lt/ReNewPoNe/pairwise/save/overall/iter_5432_merge_hf \
    --max-shard-size 2GB

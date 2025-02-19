#!/bin/bash

CUDA_VISIBLE_DEVICES=4 xtuner convert pth_to_hf \
    scripts/baseline.py \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_1_20250218/iter_12414.pth \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_1_20250218/iter_12414_hf

CUDA_VISIBLE_DEVICES=4 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_1_20250218/iter_12414_hf \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_1_20250218/iter_12414_merge_hf \
    --max-shard-size 2GB

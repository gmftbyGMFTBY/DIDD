#!/bin/bash

CUDA_VISIBLE_DEVICES=0 xtuner convert pth_to_hf \
    scripts/overall_dis.py \
    /home/lt/ReNewPoNe/pairwise/save/overall_dis/iter_3552.pth \
    /home/lt/ReNewPoNe/pairwise/save/overall_dis/iter_3552_hf

CUDA_VISIBLE_DEVICES=0 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/pairwise/save/overall_dis/iter_3552_hf \
    /home/lt/ReNewPoNe/pairwise/save/overall_dis/iter_3552_merge_hf \
    --max-shard-size 2GB

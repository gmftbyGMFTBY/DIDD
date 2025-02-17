#!/bin/bash

CUDA_VISIBLE_DEVICES=3 xtuner convert pth_to_hf \
    scripts/autoj.py \
    /home/lt/ReNewPoNe/baseline/save/autoj_ours/iter_3840.pth \
    /home/lt/ReNewPoNe/baseline/save/autoj_ours/iter_3840_hf


CUDA_VISIBLE_DEVICES=3 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/baseline/save/autoj_ours/iter_3840_hf \
    /home/lt/ReNewPoNe/baseline/save/autoj_ours/iter_3840_merge_hf \
    --max-shard-size 2GB

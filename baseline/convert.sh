#!/bin/bash

CUDA_VISIBLE_DEVICES=3 xtuner convert pth_to_hf \
    scripts/ultracm.py \
    /home/lt/ReNewPoNe/baseline/save/ultracm_ours/iter_3980.pth \
    /home/lt/ReNewPoNe/baseline/save/ultracm_ours/iter_3980_hf

CUDA_VISIBLE_DEVICES=3 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/baseline/save/ultracm_ours/iter_3980_hf \
    /home/lt/ReNewPoNe/baseline/save/ultracm_ours/iter_3980_merge_hf \
    --max-shard-size 2GB

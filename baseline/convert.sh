#!/bin/bash

CUDA_VISIBLE_DEVICES=0 xtuner convert pth_to_hf \
    scripts/ultracm.py \
    /home/lt/ReNewPoNe/baseline/save/ultracm_large_5000/iter_9946.pth \
    /home/lt/ReNewPoNe/baseline/save/ultracm_large_5000/iter_9946_hf

CUDA_VISIBLE_DEVICES=0 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/baseline/save/ultracm_large_5000/iter_9946_hf \
    /home/lt/ReNewPoNe/baseline/save/ultracm_large_5000/iter_9946_merge_hf \
    --max-shard-size 2GB

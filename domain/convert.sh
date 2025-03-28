#!/bin/bash

CUDA_VISIBLE_DEVICES=0 xtuner convert pth_to_hf \
    scripts/dis.py \
    /home/lt/ReNewPoNe/domain/save_20250322/dis/iter_11140.pth \
    /home/lt/ReNewPoNe/domain/save_20250322/dis/iter_11140_hf

CUDA_VISIBLE_DEVICES=0 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/domain/save_20250322/dis/iter_11140_hf \
    /home/lt/ReNewPoNe/domain/save_20250322/dis/iter_11140_merge_hf \
    --max-shard-size 2GB

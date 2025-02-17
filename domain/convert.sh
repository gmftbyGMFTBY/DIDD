#!/bin/bash

CUDA_VISIBLE_DEVICES=2 xtuner convert pth_to_hf \
    scripts/overall.py \
    /home/lt/ReNewPoNe/domain/save_analysis/functional_writing/iter_6000.pth \
    /home/lt/ReNewPoNe/domain/save_analysis/functional_writing/iter_6000_hf

CUDA_VISIBLE_DEVICES=2 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/domain/save_analysis/functional_writing/iter_6000_hf \
    /home/lt/ReNewPoNe/domain/save_analysis/functional_writing/iter_6000_merge_hf \
    --max-shard-size 2GB

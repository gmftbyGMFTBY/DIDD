#!/bin/bash

CUDA_VISIBLE_DEVICES=2 xtuner convert pth_to_hf \
    scripts/overall.py \
    /home/lt/ReNewPoNe/response_quality/save_baseline/baseline_8000/iter_7488.pth \
    /home/lt/ReNewPoNe/response_quality/save_baseline/baseline_8000/iter_7488_hf

CUDA_VISIBLE_DEVICES=2 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/response_quality/save_baseline/baseline_8000/iter_7488_hf \
    /home/lt/ReNewPoNe/response_quality/save_baseline/baseline_8000/iter_7488_merge_hf \
    --max-shard-size 2GB

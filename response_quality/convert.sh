#!/bin/bash

CUDA_VISIBLE_DEVICES=3 xtuner convert pth_to_hf \
    scripts/overall.py \
    /home/lt/ReNewPoNe/response_quality/save_v7/overall_v8/iter_10356.pth \
    /home/lt/ReNewPoNe/response_quality/save_v7/overall_v8/iter_10356_hf

CUDA_VISIBLE_DEVICES=3 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/response_quality/save_v7/overall_v8/iter_10356_hf \
    /home/lt/ReNewPoNe/response_quality/save_v7/overall_v8/iter_10356_merge_hf \
    --max-shard-size 2GB

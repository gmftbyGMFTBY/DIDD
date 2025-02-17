#!/bin/bash

CUDA_VISIBLE_DEVICES=3 xtuner convert pth_to_hf \
    scripts/baseline.py \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_0_v2/iter_9940.pth \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_0_v2/iter_9940_hf


CUDA_VISIBLE_DEVICES=3 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_0_v2/iter_9940_hf \
    /home/lt/ReNewPoNe/framework/save/baseline_iter_0_v2/iter_9940_merge_hf \
    --max-shard-size 2GB

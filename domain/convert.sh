#!/bin/bash

CUDA_VISIBLE_DEVICES=7 xtuner convert pth_to_hf \
    scripts/overall.py \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/overall_weak_4/iter_6080.pth \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/overall_weak_4/iter_6080_hf

CUDA_VISIBLE_DEVICES=7 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/overall_weak_4/iter_6080_hf \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/overall_weak_4/iter_6080_merge_hf \
    --max-shard-size 2GB

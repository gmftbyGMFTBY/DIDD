#!/bin/bash

CUDA_VISIBLE_DEVICES=3 xtuner convert pth_to_hf \
    scripts/overall.py \
    /home/lt/ReNewPoNe/response_quality/save_v4/overall_v6/iter_10336.pth \
    /home/lt/ReNewPoNe/response_quality/save_v4/overall_v6/iter_10336_hf

CUDA_VISIBLE_DEVICES=3 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/response_quality/save_v4/overall_v6/iter_10336_hf \
    /home/lt/ReNewPoNe/response_quality/save_v4/overall_v6/iter_10336_merge_hf \
    --max-shard-size 2GB

rm -rf /home/lt/ReNewPoNe/response_quality/save_v4/overall_v6/iter_10336.pth
rm -rf /home/lt/ReNewPoNe/response_quality/save_v4/overall_v6/iter_10336_hf

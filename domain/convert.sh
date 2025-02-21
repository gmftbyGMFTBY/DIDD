#!/bin/bash

CUDA_VISIBLE_DEVICES=2 xtuner convert pth_to_hf \
    scripts/overall.py \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_dis/iter_5570.pth \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_dis/iter_5570_hf

CUDA_VISIBLE_DEVICES=2 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_dis/iter_5570_hf \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_dis/iter_5570_merge_hf \
    --max-shard-size 2GB

rm -rf /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_dis/iter_5570.pth
rm -rf /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_dis/iter_5570_hf

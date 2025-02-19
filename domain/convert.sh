#!/bin/bash

CUDA_VISIBLE_DEVICES=2 xtuner convert pth_to_hf \
    scripts/overall.py \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_uniform/iter_2160.pth \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_uniform/iter_2160_hf

CUDA_VISIBLE_DEVICES=2 xtuner convert merge \
    /home/lt/NewPoNe/model/internlm2-7b-chat \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_uniform/iter_2160_hf \
    /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_uniform/iter_2160_merge_hf \
    --max-shard-size 2GB

rm -rf /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_uniform/iter_2160.pth
rm -rf /home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_uniform/iter_2160_hf

#!/bin/bash

##### response quality
low=/home/lt/ReNewPoNe/response_quality/save_v2/low/iter_7840_merge_hf
medium=/home/lt/ReNewPoNe/response_quality/save_v3/medium/iter_5214_merge_hf
high=/home/lt/ReNewPoNe/response_quality/save_v2/high/iter_7582_merge_hf
overall_response_quality=/home/lt/ReNewPoNe/response_quality/save_v2/overall/iter_10450_merge_hf
baseline_iter_0=/home/lt/ReNewPoNe/framework/save/baseline_iter_0/iter_7498_merge_hf
baseline=/home/lt/ReNewPoNe/framework/save/baseline/iter_5650_merge_hf
baseline_iter_0_v2=/home/lt/ReNewPoNe/framework/save/baseline_iter_0_v2/iter_9940_merge_hf

baseline_autoj=/home/lt/ReNewPoNe/baseline/save/autoj_ours/iter_3840_merge_hf

#models=($low $medium $high $overall_response_quality)
#labels=(low medium high overall_response_quality)
models=($baseline_autoj)
labels=(baseline_autoj)

for index in $(seq 0 0)
do
    model=${models[$index]}
    label=${labels[$index]}
    index=$(($index+3))
    echo "Infer $model with $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=$index python evaluate.py --available_gpus $index --tasks Q --hf_critic_model $model --prompt_type zs-crit-cot --enable_code_execution --output_dir framework/$label &
done


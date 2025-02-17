#!/bin/bash



#high=/home/lt/ReNewPoNe/response_quality/save/high/iter_9726_merge_hf
#medium=/home/lt/ReNewPoNe/response_quality/save/medium/iter_8874_merge_hf
#low=/home/lt/ReNewPoNe/response_quality/save/low/iter_9764_merge_hf
#overall=/home/lt/ReNewPoNe/response_quality/save/overall/iter_9858_merge_hf

overall=/home/lt/ReNewPoNe/response_quality/save_v2/overall/iter_10450_merge_hf
high=/home/lt/ReNewPoNe/response_quality/save_v2/high/iter_7582_merge_hf
medium=/home/lt/ReNewPoNe/response_quality/save_v3/medium/iter_5214_merge_hf
low=/home/lt/ReNewPoNe/response_quality/save_v2/low/iter_7840_merge_hf

baseline_iter_0=/home/lt/ReNewPoNe/framework/save/baseline_iter_0/iter_7498_merge_hf
baseline=/home/lt/ReNewPoNe/framework/save/baseline/iter_5650_merge_hf
baseline_iter_0_v2=/home/lt/ReNewPoNe/framework/save/baseline_iter_0_v2/iter_9940_merge_hf

baseline_autoj=/home/lt/ReNewPoNe/baseline/save/autoj_ours/iter_3840_merge_hf


#models=($overall $high $low)
#labels=(overall high low)

#models=($medium)
#labels=(medium)

models=($baseline_autoj)
labels=(baseline_autoj)

for index in $(seq 0 0)
do
    model=${models[$index]}
    label=${labels[$3ndex]}
    index=$(($index+1))
    echo "Inference $model on GPU[$index]; save into save/$label"
    CUDA_VISIBLE_DEVICES=$index python feedback_models.py --model_name $model --output_dir save_framework/$label --split dev &
    index=$(($index+1))
    CUDA_VISIBLE_DEVICES=$index python feedback_models.py --model_name $model --output_dir save_framework/$label --split test &
done

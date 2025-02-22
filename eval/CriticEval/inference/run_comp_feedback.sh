#!/bin/bash


easy=/home/lt/ReNewPoNe/pairwise/save/easy/iter_1284_merge_hf
hard_1=/home/lt/ReNewPoNe/pairwise/save/hard_1/iter_3616_merge_hf
hard_2=/home/lt/ReNewPoNe/pairwise/save/hard_2/iter_2028_merge_hf
overall_dis=/home/lt/ReNewPoNe/pairwise/save/overall_dis/iter_3552_merge_hf
comp_baseline_iter_0=/home/lt/ReNewPoNe/framework/save/comp_baseline_iter_0/iter_5286_merge_hf
comp_baseline_iter_0_v2=/home/lt/ReNewPoNe/framework/save/comp_baseline_iter_0_v2/iter_10016_merge_hf

models=($comp_baseline_iter_0_v2)
labels=(comp_baseline_iter_0_v2)
for index in $(seq 0 0)
do
    model=${models[$index]}
    label=${labels[$index]}
    index=$(($index+0))
    echo "Inference $model on GPU[$index]; save into save/$label"
    CUDA_VISIBLE_DEVICES=$index python comp_feedback_models.py --model_name $model --output_dir save_comp/$label --split test &
    CUDA_VISIBLE_DEVICES=$(($index+1)) python comp_feedback_models.py --model_name $model --output_dir save_comp/$label --split dev &
done

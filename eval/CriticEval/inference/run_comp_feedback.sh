#!/bin/bash


easy=/home/lt/ReNewPoNe/pairwise/save/easy/iter_1284_merge_hf
hard_1=/home/lt/ReNewPoNe/pairwise/save/hard_1/iter_3616_merge_hf
hard_2=/home/lt/ReNewPoNe/pairwise/save/hard_2/iter_2028_merge_hf

models=($easy $hard_1 $hard_2)
labels=(easy hard_1 hard_2)
for index in $(seq 0 2)
do
    model=${models[$index]}
    label=${labels[$index]}
    index=$(($index+3))
    echo "Inference $model on GPU[$index]; save into save/$label"
    CUDA_VISIBLE_DEVICES=$index python comp_feedback_models.py --model_name $model --output_dir save_comp/$label --split test &
done

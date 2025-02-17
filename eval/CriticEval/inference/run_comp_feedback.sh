#!/bin/bash


easy=/home/lt/ReNewPoNe/pairwise/save/easy/iter_5042_merge_hf
hard_1=/home/lt/ReNewPoNe/pairwise/save/hard_1/iter_4812_merge_hf
hard_2=/home/lt/ReNewPoNe/pairwise/save/hard_2/iter_3806_merge_hf
overall=/home/lt/ReNewPoNe/pairwise/save/overall/iter_5432_merge_hf

models=($easy $hard_1 $hard_2 $overall)
labels=(easy hard_1 hard_2 overall)
for index in $(seq 0 3)
do
    model=${models[$index]}
    label=${labels[$index]}
    index=$(($index+0))
    echo "Inference $model on GPU[$index]; save into save/$label"
    CUDA_VISIBLE_DEVICES=$index python comp_feedback_models.py --model_name $model --output_dir save_comp/$label --split dev &
done

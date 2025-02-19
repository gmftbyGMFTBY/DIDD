#!/bin/bash


baseline=scripts/baseline_iter_1.py
#autoj_ours_iter_0=scripts/autoj_ours_iter_0.py
ultracm_iter_0=scripts/ultracm_iter_0.py
autoj_with_baseline_data_iter_0=scripts/autoj_with_baseline_data_iter_0.py

baseline_num_4979=scripts/baseline_num_4979.py
baseline_num_6382=scripts/baseline_num_6382.py

cfg_files=($baseline_num_4979 $baseline_num_6382)
labels=(baseline_num_4979 baseline_num_6382)

for index in $(seq 0 0)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    echo "Train $cfg_file with label $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=4 NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save/$label &

    index=$(($index+1))
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    echo "Train $cfg_file with label $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=7 NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save/$label &
done

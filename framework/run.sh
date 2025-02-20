#!/bin/bash


baseline=scripts/baseline_iter_1.py
llama3_8b_baseline=scripts/llama3_8b_baseline.py
qwen1_5_7b_baseline=scripts/qwen1_5_7b_baseline.py
#autoj_ours_iter_0=scripts/autoj_ours_iter_0.py
ultracm_iter_0=scripts/ultracm_iter_0.py
autoj_with_baseline_data_iter_0=scripts/autoj_with_baseline_data_iter_0.py

baseline_num_4979=scripts/baseline_num_4979.py
baseline_num_6382=scripts/baseline_num_6382.py

baseline_dis_mode_raw=scripts/baseline_dis_mode_raw.py
baseline_dis_mode_new=scripts/baseline_dis_mode_new.py

cfg_files=($qwen1_5_7b_baseline)
labels=(qwen1_5_7b_baseline)

for index in $(seq 0 0)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    index=$(($index+4))
    echo "Train $cfg_file with label $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save/$label
done

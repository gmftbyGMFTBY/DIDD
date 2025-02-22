#!/bin/bash


easy=scripts/easy.py
hard_1=scripts/hard_1.py
hard_2=scripts/hard_2.py
overall=scripts/overall.py
overall_dis=scripts/overall_dis.py
baseline_comp_num_5000=scripts/baseline_comp_num_5000.py

cfg_files=($baseline_comp_num_5000)
labels=(baseline_comp_num_5000)

for index in $(seq 0 0)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    index=$(($index+6))
    echo "Train $cfg_file with label $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save/$label &
done

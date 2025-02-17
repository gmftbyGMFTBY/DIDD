#!/bin/bash


baseline=scripts/baseline_iter_0.py
cfg_files=($baseline)
labels=(baseline_iter_0_v2)

for index in $(seq 0 0)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    index=$(($index+6))
    echo "Train $cfg_file with label $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save/$label &
done

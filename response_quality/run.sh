#!/bin/bash


overall=scripts/overall.py
low=scripts/low.py
medium=scripts/medium.py
high=scripts/high.py

cfg_files=($medium $overall)
labels=(medium_v4 overall_v3)

for index in $(seq 0 0)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    echo "Train $cfg_file with label $label on GPU[1]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save_v4/$label &
done

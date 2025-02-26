#!/bin/bash


ultracm_large_5000=scripts/ultracm.py
autoj_pairwise=scripts/autoj_pairwise.py
cfg_files=($ultracm_large_5000)
labels=(ultracm_large_5000)

for index in $(seq 0 0)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    index=$(($index+0))
    echo "Train $cfg_file with label $label on GPU[1]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save/$label &
done

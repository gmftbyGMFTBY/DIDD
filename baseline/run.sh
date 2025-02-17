#!/bin/bash


ultracm=scripts/ultracm.py
cfg_files=($ultracm)
labels=(ultracm_ours)

for index in $(seq 0 0)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    index=$(($index+4))
    echo "Train $cfg_file with label $label on GPU[1]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save/$label &
done

#!/bin/bash


easy=scripts/easy.py
hard_1=scripts/hard_1.py
hard_2=scripts/hard_2.py
overall=scripts/overall.py

cfg_files=($easy $hard_1 $hard_2 $overall)
labels=(easy hard_1 hard_2 overall)

for index in $(seq 0 3)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    index=$(($index+0))
    echo "Train $cfg_file with label $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save/$label &
done

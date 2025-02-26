#!/bin/bash


overall=scripts/overall.py
overall_v5=scripts/overall_v5.py
overall_v6=scripts/overall_v6.py
overall_v7=scripts/overall_v7.py
overall_v8=scripts/overall_v8.py
low=scripts/low.py
medium=scripts/medium.py
high=scripts/high.py

###### high vs low
high_vs_low_10=scripts/high_vs_low_1.py
high_vs_low_09=scripts/high_vs_low_0.9.py
high_vs_low_08=scripts/high_vs_low_0.8.py
high_vs_low_07=scripts/high_vs_low_0.7.py
high_vs_low_06=scripts/high_vs_low_0.6.py
high_vs_low_05=scripts/high_vs_low_0.5.py
high_vs_low_04=scripts/high_vs_low_0.4.py
high_vs_low_03=scripts/high_vs_low_0.3.py
high_vs_low_02=scripts/high_vs_low_0.2.py
high_vs_low_01=scripts/high_vs_low_0.1.py
high_vs_low_00=scripts/high_vs_low_0.py


###### baseline train num exp
baseline_1000=scripts/baseline_1000.py
baseline_2000=scripts/baseline_2000.py
baseline_4000=scripts/baseline_4000.py
baseline_7000=scripts/baseline_7000.py
baseline_8000=scripts/baseline_8000.py

cfg_files=($baseline_1000 $baseline_2000 $baseline_4000 $baseline_7000 $baseline_8000)
labels=(baseline_1000 baseline_2000 baseline_4000 baseline_7000 baseline_8000)

for index in $(seq 0 4)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    echo "Train $cfg_file with label $label on GPU[$index]"
    index=$(($index+0))
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save_baseline/$label &
done

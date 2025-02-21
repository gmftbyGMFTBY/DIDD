#!/bin/bash


baseline=scripts/baseline_iter_1.py
qwen1_5_7b_baseline=scripts/qwen1_5_7b_baseline.py
#autoj_ours_iter_0=scripts/autoj_ours_iter_0.py
ultracm_iter_0=scripts/ultracm_iter_0.py
autoj_with_baseline_data_iter_0=scripts/autoj_with_baseline_data_iter_0.py

baseline_num_4979=scripts/baseline_num_4979.py
baseline_num_6382=scripts/baseline_num_6382.py

baseline_dis_mode_raw=scripts/baseline_dis_mode_raw.py
baseline_dis_mode_new=scripts/baseline_dis_mode_new.py

###### baseline mixture data exp
baseline_mixture_rate_02=scripts/baseline_mixture_rate_0.2.py
baseline_mixture_rate_04=scripts/baseline_mixture_rate_0.4.py
baseline_mixture_rate_06=scripts/baseline_mixture_rate_0.6.py
baseline_mixture_rate_08=scripts/baseline_mixture_rate_0.8.py

cfg_files=($baseline_mixture_rate_02 $baseline_mixture_rate_04 $baseline_mixture_rate_06 $baseline_mixture_rate_08)
labels=(baseline_mixture_rate_02 baseline_mixture_rate_04 baseline_mixture_rate_06 baseline_mixture_rate_08)


llama3_8b_baseline=scripts/llama3_8b_baseline.py
llama3_8b_baseline_iter_0=scripts/llama3_8b_baseline_iter_0.py
cfg_files=($llama3_8b_baseline_iter_0)
labels=($llama3_8b_baseline_iter_0)

###### test num exp
baseline_test_num_200_iter_0=scripts/baseline_test_num_200.py
baseline_test_num_800_iter_0=scripts/baseline_test_num_800.py
baseline_test_num_1000_iter_0=scripts/baseline_test_num_1000.py
cfg_files=($baseline_test_num_200_iter_0 $baseline_test_num_800_iter_0 $baseline_test_num_1000_iter_0)
labels=(baseline_test_num_200_iter_0 baseline_test_num_800_iter_0 baseline_test_num_1000_iter_0)

##### train num exp
baseline_train_num_200_iter_0=scripts/baseline_iter_0_train_num_100.py
baseline_train_num_400_iter_0=scripts/baseline_iter_0_train_num_400.py
baseline_train_num_1000_iter_0=scripts/baseline_iter_0_train_num_1000.py
baseline_train_num_4000_iter_0=scripts/baseline_iter_0_train_num_4000.py
cfg_files=($baseline_train_num_400_iter_0)
labels=(baseline_train_num_400_iter_0)


for index in $(seq 0 0)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    index=$(($index+7))
    echo "Train $cfg_file with label $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save/$label &
done

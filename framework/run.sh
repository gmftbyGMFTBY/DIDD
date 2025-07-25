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



#### 新的迭代试验
baseline_iter_1_only=scripts/baseline_iter_1.py
comp_baseline_iter_0=scripts/baseline_comp.py
# llama3-8b large num 6382 samples
llama3_8b_baseline_large=scripts/llama3_8b_baseline.py
cfg_files=($comp_baseline_iter_0)
labels=(comp_baseline_new_resquality_from_hard_2)

###### baseline comp test num
baseline_comp_test_num_100=scripts/baseline_comp_test_num_100.py
baseline_comp_test_num_200=scripts/baseline_comp_test_num_200.py
baseline_comp_test_num_300=scripts/baseline_comp_test_num_300.py
baseline_comp_test_num_400=scripts/baseline_comp_test_num_400.py
baseline_comp_test_num_500=scripts/baseline_comp_test_num_500.py
baseline_comp_test_num_600=scripts/baseline_comp_test_num_600.py
baseline_comp_test_num_700=scripts/baseline_comp_test_num_700.py
baseline_comp_test_num_800=scripts/baseline_comp_test_num_800.py
baseline_comp_test_num_900=scripts/baseline_comp_test_num_900.py
baseline_comp_test_num_1000=scripts/baseline_comp_test_num_1000.py


llama3_8b_0225_balance=scripts/llama3_8b_baseline.py
baseline_comp_20250225=scripts/baseline_comp_balance.py

#### iter exp
iter_exp_iter_0_only=scripts/iter_exp_iter_0_only.py
iter_exp_iter_01_only=scripts/iter_exp_iter_0_only.py
iter_exp_iter_012_only=scripts/iter_exp_iter_0_only.py
iter_exp_iter_0123_only=scripts/iter_exp_iter_0_only.py

#### llama3 8b instruct pairwise data
comp_data_llama3_8b=scripts/llama3_8b_baseline.py


#### llama3 pair data on internlm
comp_data_llama3_on_interlm=scripts/baseline_comp.py
cfg_files=($iter_exp_iter_0123_only)
labels=(iter_exp_iter_0123_only)

##### comp iter exp
comp_iter_0_only=scripts/comp_iter_exp.py
comp_iter_01_only=scripts/comp_iter_exp.py
comp_iter_012_only=scripts/comp_iter_exp.py

comp_iter_0_v2_only=scripts/comp_iter_exp.py
comp_iter_01_v2_only=scripts/comp_iter_exp.py
comp_iter_012_v2_only=scripts/comp_iter_exp.py

##### comp train num exp
comp_iter_0_train_num_4000=scripts/comp_iter_0_train_num_4000.py
comp_iter_0_train_num_2000=scripts/comp_iter_0_train_num_2000.py
comp_iter_0_train_num_1000=scripts/comp_iter_0_train_num_1000.py
comp_iter_0_train_num_800=scripts/comp_iter_0_train_num_800.py
comp_iter_0_train_num_400=scripts/comp_iter_0_train_num_400.py
comp_iter_0_train_num_200=scripts/comp_iter_0_train_num_200.py

models=($comp_iter_0_train_num_4000 $comp_iter_0_train_num_2000 $comp_iter_0_train_num_1000 $comp_iter_0_train_num_800 $comp_iter_0_train_num_400 $comp_iter_0_train_num_200)
labels=(comp_iter_0_train_num_4000 comp_iter_0_train_num_2000 comp_iter_0_train_num_1000 comp_iter_0_train_num_800 comp_iter_0_train_num_400 comp_iter_0_train_num_200)

cfg_files=($comp_iter_012_v2_only)
labels=(comp_iter_012_v2_only)


##### pairwise test num scaling
pairwise_test_scaling_1000=scripts/pairwise_test_scaling_1000.py
pairwise_test_scaling_800=scripts/pairwise_test_scaling_800.py
pairwise_test_scaling_500=scripts/pairwise_test_scaling_500.py
pairwise_test_scaling_400=scripts/pairwise_test_scaling_400.py
pairwise_test_scaling_200=scripts/pairwise_test_scaling_200.py
pairwise_test_scaling_100=scripts/pairwise_test_scaling_100.py

cfg_files=($pairwise_test_scaling_1000 $pairwise_test_scaling_800 $pairwise_test_scaling_500 $pairwise_test_scaling_400 $pairwise_test_scaling_200 $pairwise_test_scaling_100)
labels=(pairwise_test_scaling_1000 pairwise_test_scaling_800 pairwise_test_scaling_500 pairwise_test_scaling_400 pairwise_test_scaling_200 pairwise_test_scaling_100)
cfg_files=(scripts/llama3_8b_baseline_reverse.py)
labels=(llama3_8b_baseline_reverse)

cfg_files=(scripts/llama3_8b_baseline_reverse.py scripts/llama3_8b_baseline_single_reverse.py)
labels=(llama3_8b_baseline_reverse llama3_8b_baseline_single_reverse)

cfg_files=(scripts/internlm2_7b_baseline_single_reverse.py scripts/internlm2_7b_baseline_reverse.py)
labels=(internlm2_7b_baseline_single_reverse internlm2_7b_baseline_reverse)

####### revision
cfg_files=(scripts/qwen2_5_1_5b_baseline.py)
labels=(qwen2_5_1_5b_iter_0)

cfg_files=(scripts/comp_iter_0_train_num_2000_qwen2.5-0.5b.py scripts/comp_iter_0_train_num_2000_qwen2.5-7b.py)
labels=(qwen2_5_3b_iter_0 qwen2_5_7b_iter_0)

for index in $(seq 0 1)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    index=$(($index+6))
    echo "Train $cfg_file with label $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir revision_20250715_pairwise_save/$label &
done

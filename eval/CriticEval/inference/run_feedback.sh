#!/bin/bash



#high=/home/lt/ReNewPoNe/response_quality/save/high/iter_9726_merge_hf
#medium=/home/lt/ReNewPoNe/response_quality/save/medium/iter_8874_merge_hf
#low=/home/lt/ReNewPoNe/response_quality/save/low/iter_9764_merge_hf
#overall=/home/lt/ReNewPoNe/response_quality/save/overall/iter_9858_merge_hf

overall=/home/lt/ReNewPoNe/response_quality/save_v2/overall/iter_10450_merge_hf
high=/home/lt/ReNewPoNe/response_quality/save_v2/high/iter_7582_merge_hf
medium=/home/lt/ReNewPoNe/response_quality/save_v3/medium/iter_5214_merge_hf
low=/home/lt/ReNewPoNe/response_quality/save_v2/low/iter_7840_merge_hf

baseline_iter_0=/home/lt/ReNewPoNe/framework/save/baseline_iter_0/iter_7498_merge_hf
baseline=/home/lt/ReNewPoNe/framework/save/baseline/iter_5650_merge_hf
baseline_iter_0_v2=/home/lt/ReNewPoNe/framework/save/baseline_iter_0_v2/iter_9940_merge_hf

baseline_autoj=/home/lt/ReNewPoNe/baseline/save/autoj_ours/iter_3840_merge_hf
baseline_ultracm=/home/lt/ReNewPoNe/baseline/save/ultracm_ours/iter_3980_merge_hf

###### domain analysis
code=/home/lt/ReNewPoNe/domain/save_analysis/code/iter_3928_merge_hf
exam_question=/home/lt/ReNewPoNe/domain/save_analysis/exam_question/iter_6000_merge_hf
general_communication=/home/lt/ReNewPoNe/domain/save_analysis/general_communication/iter_3772_merge_hf
summarization=/home/lt/ReNewPoNe/domain/save_analysis/summarization/iter_1220_merge_hf
creative_writing=/home/lt/ReNewPoNe/domain/save_analysis/creating_writing/iter_4800_merge_hf
functional_writing=/home/lt/ReNewPoNe/domain/save_analysis/functional_writing/iter_6000_merge_hf
rewriting=/home/lt/ReNewPoNe/domain/save_analysis/rewriting/iter_2160_merge_hf

##### response quality high-vs-low analysis
high_vs_low_10=/home/lt/ReNewPoNe/response_quality/save_high_vs_low/high_vs_low_10/iter_5876_merge_hf
high_vs_low_09=/home/lt/ReNewPoNe/response_quality/save_high_vs_low/high_vs_low_09/iter_5884_merge_hf
high_vs_low_08=/home/lt/ReNewPoNe/response_quality/save_high_vs_low/high_vs_low_08/iter_5876_merge_hf

models=($high_vs_low_10 $high_vs_low_09 $high_vs_low_08)
labels=(high_vs_low_10 high_vs_low_09 high_vs_low_08)

##### response quality overall-v4-v5
rq_overall_v5=/home/lt/ReNewPoNe/response_quality/save_v4/overall_v5/iter_10340_merge_hf
rq_overall_v6=/home/lt/ReNewPoNe/response_quality/save_v4/overall_v6/iter_10336_merge_hf

models=($rq_overall_v5 $rq_overall_v6)
labels=(overall_v5 overall_v6)

##### domain strategy
dis=/home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_dis/iter_2160_merge_hf
uniform=/home/lt/ReNewPoNe/domain/save_domain_strategy/domain_strategy_uniform/iter_2160_merge_hf
models=($dis $uniform)
labels=(dis uniform)

##### framework autoj_ours_iter_0
autoj_ours_iter_0_e1=/home/lt/ReNewPoNe/framework/save/autoj_ours_iter_0_e1/iter_1955_merge_hf
autoj_with_baseline_data_iter_0=/home/lt/ReNewPoNe/framework/save/autoj_with_baseline_data_iter_0/iter_2939_merge_hf
ultracm_iter_0=/home/lt/ReNewPoNe/framework/save/ultracm_iter_0_20250218/iter_6960_merge_hf
baseline_20250218=/home/lt/ReNewPoNe/framework/save/baseline_20250218/iter_9608_merge_hf
baseline_iter_1_20250218=/home/lt/ReNewPoNe/framework/save/baseline_iter_1_20250218/iter_12414_merge_hf
baseline_num_4979=/home/lt/ReNewPoNe/framework/save/baseline_num_4979/iter_9368_merge_hf
baseline_num_6382=/home/lt/ReNewPoNe/framework/save/baseline_num_6382/iter_11990_merge_hf

baseline_dis_mode_raw=/home/lt/ReNewPoNe/framework/save/baselien_dis_mode_raw/iter_8206_merge_hf
baseline_dis_mode_new=/home/lt/ReNewPoNe/framework/save/baseline_dis_mode_new/iter_8206_merge_hf

llama3_8b_baseline=/home/lt/ReNewPoNe/framework/save/llama3_8b_baseline/iter_5676_merge_hf
llama3_8b_baseline_iter_0=/home/lt/ReNewPoNe/framework/save/llama3_8b_baseline_iter_0/iter_8484_merge_hf
qwen15_7b_baseline=/home/lt/ReNewPoNe/framework/save/qwen1_5_7b_baseline/iter_5678_merge_hf

####### mixture rate exp
baseline_mixture_02=/home/lt/ReNewPoNe/framework/save/baseline_mixture_rate_02/iter_8620_merge_hf
baseline_mixture_04=/home/lt/ReNewPoNe/framework/save/baseline_mixture_rate_04/iter_8484_merge_hf
baseline_mixture_06=/home/lt/ReNewPoNe/framework/save/baseline_mixture_rate_06/iter_8508_merge_hf
baseline_mixture_08=/home/lt/ReNewPoNe/framework/save/baseline_mixture_rate_08/iter_8528_merge_hf

models=($baseline_mixture_02 $baseline_mixture_04 $baseline_mixture_06 $baseline_mixture_08)
labels=(baseline_mixture_02 baseline_mixture_04 baseline_mixture_06 baseline_mixture_08)

###### test num exp
baseline_test_num_200=/home/lt/ReNewPoNe/framework/save/baseline_test_num_200_iter_0/iter_8624_merge_hf
baseline_test_num_800=/home/lt/ReNewPoNe/framework/save/baseline_test_num_800_iter_0/iter_8554_merge_hf
baseline_test_num_1000=/home/lt/ReNewPoNe/framework/save/baseline_test_num_1000_iter_0/iter_8532_merge_hf
models=($baseline_test_num_200 $baseline_test_num_800 $baseline_test_num_1000)
labels=(baseline_test_num_200 baseline_test_num_800 baseline_test_num_1000)

###### train num exp
baseline_train_num_200=/home/lt/ReNewPoNe/framework/save/baseline_train_num_200_iter_0/iter_6050_merge_hf
baseline_train_num_400=/home/lt/ReNewPoNe/framework/save/baseline_train_num_400_iter_0/iter_6450_merge_hf
baseline_train_num_1000=/home/lt/ReNewPoNe/framework/save/baseline_train_num_1000_iter_0/iter_7650_merge_hf
baseline_train_num_4000=/home/lt/ReNewPoNe/framework/save/baseline_train_num_4000_iter_0/iter_12682_merge_hf

####
baseline_iter_1_only=/home/lt/ReNewPoNe/framework/save/baseline_iter_1_only/iter_2806_merge_hf

##### domain overall strong and weak 4
overall_strong_4=/home/lt/ReNewPoNe/domain/save_domain_strategy/overall_strong_4/iter_5448_merge_hf
overall_weak_4=/home/lt/ReNewPoNe/domain/save_domain_strategy/overall_weak_4/iter_6080_merge_hf

##### response overall v78
overall_v7=/home/lt/ReNewPoNe/response_quality/save_v7/overall_v7/iter_10350_merge_hf
overall_v8=/home/lt/ReNewPoNe/response_quality/save_v7/overall_v8/iter_10356_merge_hf

###### baseline scaling training num
baseline_1000=/home/lt/ReNewPoNe/response_quality/save_baseline/baseline_1000/iter_1866_merge_hf
baseline_2000=/home/lt/ReNewPoNe/response_quality/save_baseline/baseline_2000/iter_3786_merge_hf
baseline_4000=/home/lt/ReNewPoNe/response_quality/save_baseline/baseline_4000/iter_7504_merge_hf
baseline_7000=/home/lt/ReNewPoNe/response_quality/save_baseline/baseline_7000/iter_6557_merge_hf
baseline_8000=/home/lt/ReNewPoNe/response_quality/save_baseline/baseline_8000/iter_7488_merge_hf

models=($baseline_1000 $baseline_2000 $baseline_4000 $baseline_7000 $baseline_8000)
labels=(baseline_1000 baseline_2000 baseline_4000 baseline_7000 baseline_8000)

#### base models
internlm2=/home/lt/NewPoNe/model/internlm2-7b-chat
llama3=/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct
qwen=/home/lt/models/Qwen2-7B-Instruct
llama3_8b_baseline_large=/home/lt/ReNewPoNe/framework/save/llama3_8b_baseline_large/iter_6022_merge_hf

ultracm_large_5000=/home/lt/ReNewPoNe/baseline/save/ultracm_large_5000/iter_9946_merge_hf

models=($ultracm_large_5000)
labels=(ultracm_large_5000)

###### comp baseline test num
comp_baseline_test_num_100=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_100/iter_1373_merge_hf
comp_baseline_test_num_200=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_200/iter_2161_merge_hf
comp_baseline_test_num_300=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_300/iter_2485_merge_hf
comp_baseline_test_num_400=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_400/iter_3174_merge_hf
comp_baseline_test_num_500=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_500/iter_3885_merge_hf
comp_baseline_test_num_600=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_600/iter_4483_merge_hf
comp_baseline_test_num_1000=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_1000/iter_7051_merge_hf

models=($comp_baseline_test_num_100 $comp_baseline_test_num_200 $comp_baseline_test_num_300 $comp_baseline_test_num_400 $comp_baseline_test_num_500 $comp_baseline_test_num_600 $comp_baseline_test_num_1000)

data_mixture_rate_06_8508_iter_1=/home/lt/ReNewPoNe/framework/save/data_mixture_rate_06_8508_iter_1/iter_1000_merge_hf
models=($data_mixture_rate_06_8508_iter_1)
labels=(data_mixture_rate_06_8508_iter_1)


######## iter_exp
iter_0=/home/lt/ReNewPoNe/framework/save/iter_exp_iter_01_only/iter_3914_merge_hf
iter_01=/home/lt/ReNewPoNe/framework/save/iter_exp_iter_0_only/iter_1950_merge_hf
iter_012=/home/lt/ReNewPoNe/framework/save/iter_exp_iter_012_only/iter_5864_merge_hf
models=($iter_012)
labels=(iter_012)

models=(skywork-reward-8b)
labels=(skyword-reward-8b)

models=(internlm2-20b-reward)
labels=(internlm2-20b-reward)

models=(/home/lt/ReNewPoNe/domain/save_20250322/uniform/iter_11668_merge_hf /home/lt/ReNewPoNe/domain/save_20250322/dis/iter_11140_merge_hf)
labels=(uniform dis)

models=(internlm2-8b-reward)
labels=(internlm2-8b-reward)

models=(grm-3b)
labels=(grm-3b)

#### reverse dis exp
llama3_reverse_dis=/home/lt/ReNewPoNe/framework/save_pairwise_reverse/llama3_8b_baseline_single_reverse/iter_7676_merge_hf
internlm2_reverse_dis=/home/lt/ReNewPoNe/framework/save_pairwise_reverse/internlm2_7b_baseline_single_reverse/iter_7650_merge_hf
models=($internlm2_reverse_dis)
labels=(internlm2_reverse_dis)


####### revision  20250715
models=(/home/lt/ReNewPoNe/framework/revision_20250715_qwen2/qwen2_0_5b_baseline/iter_5678_merge_hf /home/lt/Qwen/Qwen2-0.5B-Instruct /home/lt/ReNewPoNe/framework/revision_20250715_qwen2/qwen2_0_5b_iter_0/iter_7678_merge_hf)
labels=(qwen2_0_5b_baseline qwen2_0_5b qwen2_0_5b_iter_0)


models=(/home/lt/Qwen/Qwen2.5-0.5B-Instruct /home/lt/ReNewPoNe/framework/revision_20250715_save/qwen2_5_0_5b_single_baseline/iter_5678_merge_hf /home/lt/ReNewPoNe/framework/revision_20250715_save/qwen2_5_0_5b_iter_0_v2/iter_7678_merge_hf)
labels=(qwen2_5_0_5b qwen2_5_0_5b_baseline qwen2_5_0_5b_iter)

models=(/home/lt/Qwen/Qwen2.5-1.5B-Instruct /home/lt/ReNewPoNe/framework/revision_20250715_save/qwen2_5_1_5b_single_baseline/iter_5678_merge_hf /home/lt/ReNewPoNe/framework/revision_20250715_save/qwen2_5_1_5b_iter_0/iter_7678_merge_hf)
labels=(qwen2_5_1_5b qwen2_5_1_5b_baseline qwen2_5_1_5b_iter_0)

models=(/home/lt/Qwen/Qwen2.5-3B-Instruct /home/lt/ReNewPoNe/framework/revision_20250715_save/qwen2_5_3b_single_baseline/iter_5678_merge_hf /home/lt/ReNewPoNe/framework/revision_20250715_save/qwen2_5_3b_iter_0/iter_7678_merge_hf)
labels=(qwen2_5_3b qwen2_5_3b_baseline qwen2_5_3b_iter_0)

#models=(/home/lt/Qwen/Qwen2.5-7B-Instruct /home/lt/ReNewPoNe/framework/revision_20250715_save/qwen2_5_7b_baseline/iter_5678_merge_hf /home/lt/ReNewPoNe/framework/revision_20250715_save/qwen2_5_7b_iter_0/iter_7678_merge_hf)
#labels=(qwen2_5_7b qwen2_5_7b_baseline qwen2_5_7b_iter_0)

for index in $(seq 0 2)
do
    model=${models[$index]}
    label=${labels[$index]}
    index=$(($index+0))
    echo "Inference $model on GPU[$index]; save into save/$label"
    #CUDA_VISIBLE_DEVICES=2 python feedback_models.py --model_name $model --output_dir revision_20250715_qwen2_feedback/$label --split dev
    CUDA_VISIBLE_DEVICES=3 python feedback_models.py --model_name $model --output_dir revision_20250715_qwen2_feedback/$label --split test
done

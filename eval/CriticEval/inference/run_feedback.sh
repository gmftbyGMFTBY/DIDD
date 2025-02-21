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

models=($baseline_train_num_4000)
labels=(baseline_train_num_4000)

for index in $(seq 0 0)
do
    model=${models[$index]}
    label=${labels[$index]}
    echo "Inference $model on GPU[$index]; save into save/$label"
    CUDA_VISIBLE_DEVICES=$(($index+0)) python feedback_models.py --model_name $model --output_dir save_framework/$label --split test &
done

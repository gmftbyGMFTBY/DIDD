#!/bin/bash


##### response quality
model=/home/lt/ReNewPoNe/response_quality/save_v2/low/iter_7840_merge_hf

low_file=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality/low/_home_lt_ReNewPoNe_response_quality_save_v2_low_iter_7840_merge_hf/critique/result_02_16_14_14_28.jsonl
medium_file=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality/medium/_home_lt_ReNewPoNe_response_quality_save_v3_medium_iter_5214_merge_hf/critique/result_02_16_14_15_44.jsonl
high_file=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality/high/_home_lt_ReNewPoNe_response_quality_save_v2_high_iter_7582_merge_hf/critique/result_02_16_14_15_11.jsonl
overall_file=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality/overall_response_quality/_home_lt_ReNewPoNe_response_quality_save_v2_overall_iter_10450_merge_hf/critique/result_02_16_14_16_10.jsonl

baseline_iter_0=/home/lt/ReNewPoNe/eval/CriticBench/src/framework/baseline/_home_lt_ReNewPoNe_framework_save_baseline_iter_5650_merge_hf/critique/result_02_16_15_27_09.jsonl
baseline=/home/lt/ReNewPoNe/eval/CriticBench/src/framework/baseline_iter_0/_home_lt_ReNewPoNe_framework_save_baseline_iter_0_iter_7498_merge_hf/critique/result_02_16_15_27_04.jsonl
baseline_iter_0_v2=/home/lt/ReNewPoNe/eval/CriticBench/src/framework/baseline_iter_0_v2/_home_lt_ReNewPoNe_framework_save_baseline_iter_0_v2_iter_9940_merge_hf/critique/result_02_16_20_45_50.jsonl
baseline_autoj=/home/lt/ReNewPoNe/eval/CriticBench/src/framework/baseline_autoj/_home_lt_ReNewPoNe_baseline_save_autoj_ours_iter_3840_merge_hf/critique/result_02_17_09_46_28.jsonl
baseline_ultracm=/home/lt/ReNewPoNe/eval/CriticBench/src/framework/baseline_ultracm/_home_lt_ReNewPoNe_baseline_save_ultracm_ours_iter_3980_merge_hf/critique/result_02_17_11_12_04.jsonl

##### domain analysis
code=/home/lt/ReNewPoNe/eval/CriticBench/src/domain_analysis/code/_home_lt_ReNewPoNe_domain_save_analysis_code_iter_3928_merge_hf/critique/result_02_17_17_55_46.jsonl
exam_question=/home/lt/ReNewPoNe/eval/CriticBench/src/domain_analysis/exam_question/_home_lt_ReNewPoNe_domain_save_analysis_exam_question_iter_6000_merge_hf/critique/result_02_17_17_53_40.jsonl
general_communication=/home/lt/ReNewPoNe/eval/CriticBench/src/domain_analysis/general_communication/_home_lt_ReNewPoNe_domain_save_analysis_general_communication_iter_3772_merge_hf/critique/result_02_17_17_54_12.jsonl
summarization=/home/lt/ReNewPoNe/eval/CriticBench/src/domain_analysis/summarization/_home_lt_ReNewPoNe_domain_save_analysis_summarization_iter_1220_merge_hf/critique/result_02_17_17_56_28.jsonl
creative_writing=/home/lt/ReNewPoNe/eval/CriticBench/src/domain_analysis/creative_writing/_home_lt_ReNewPoNe_domain_save_analysis_creating_writing_iter_4800_merge_hf/critique/result_02_17_17_53_48.jsonl
functional_writing=/home/lt/ReNewPoNe/eval/CriticBench/src/domain_analysis/functional_writing/_home_lt_ReNewPoNe_domain_save_analysis_functional_writing_iter_6000_merge_hf/critique/result_02_17_17_57_32.jsonl
rewriting=/home/lt/ReNewPoNe/eval/CriticBench/src/domain_analysis/rewriting/_home_lt_ReNewPoNe_domain_save_analysis_rewriting_iter_2160_merge_hf/critique/result_02_17_17_56_12.jsonl

##### response quality analysis
medium_v4=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality_analysis/medium_v4/_home_lt_ReNewPoNe_response_quality_save_v4_medium_v4_iter_10356_merge_hf/critique/result_02_17_20_27_58.jsonl
overall_v3=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality_analysis/overall_v3/_home_lt_ReNewPoNe_response_quality_save_v4_overall_v3_iter_10350_merge_hf/critique/result_02_17_20_27_07.jsonl
overall_v4=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality_analysis/overall_v4/_home_lt_ReNewPoNe_response_quality_save_v4_overall_v4_iter_10330_merge_hf/critique/result_02_17_20_26_01.jsonl

#files=($code $exam_question $general_communication $summarization $creative_writing $functional_writing $rewriting)
#labels=(code exam_question general_communication summarization creative_writing functional_writing rewriting)
files=($medium_v4 $overall_v3 $overall_v4)
labels=(medium_v4 overall_v3 overall_v4)

##### domain strategy dis
dis=/home/lt/ReNewPoNe/eval/CriticBench/src/domain_strategy_analysis/dis/_home_lt_ReNewPoNe_domain_save_domain_strategy_domain_strategy_dis_iter_2160_merge_hf/critique/result_02_18_10_08_29.jsonl
uniform=/home/lt/ReNewPoNe/eval/CriticBench/src/domain_strategy_analysis/uniform/_home_lt_ReNewPoNe_domain_save_domain_strategy_domain_strategy_uniform_iter_2160_merge_hf/critique/result_02_18_10_09_15.jsonl

files=($dis $uniform)
labels=(dis uniform)

##### response quality v56
rq_overall_v5=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality_analysis/overall_v5/_home_lt_ReNewPoNe_response_quality_save_v4_overall_v5_iter_10340_merge_hf/critique/result_02_18_10_09_39.jsonl
rq_overall_v6=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality_analysis/overall_v6/_home_lt_ReNewPoNe_response_quality_save_v4_overall_v6_iter_10336_merge_hf/critique/result_02_18_10_09_21.jsonl
files=($rq_overall_v5 $rq_overall_v6)
labels=(rq_overall_v5 rq_overall_v6)

##### high-vs-low
high_vs_low_10=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality_analysis/high_vs_low_10/_home_lt_ReNewPoNe_response_quality_save_high_vs_low_high_vs_low_10_iter_5876_merge_hf/critique/result_02_18_10_13_14.jsonl
high_vs_low_09=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality_analysis/high_vs_low_09/_home_lt_ReNewPoNe_response_quality_save_high_vs_low_high_vs_low_09_iter_5884_merge_hf/critique/result_02_18_10_06_30.jsonl
high_vs_low_08=/home/lt/ReNewPoNe/eval/CriticBench/src/response_quality_analysis/high_vs_low_08/_home_lt_ReNewPoNe_response_quality_save_high_vs_low_high_vs_low_08_iter_5876_merge_hf/critique/result_02_18_10_09_37.jsonl

files=($high_vs_low_10 $high_vs_low_09 $high_vs_low_08)
labels=(high_vs_low_10 high_vs_low_09 high_vs_low_08)

baseline_20250218=/home/lt/ReNewPoNe/eval/CriticBench/src/save_framework/baseline_20250218/_home_lt_ReNewPoNe_framework_save_baseline_20250218_iter_9608_merge_hf/critique/result_02_19_08_59_21.jsonl
baseline_iter_1_20250218=/home/lt/ReNewPoNe/eval/CriticBench/src/save_framework/baseline_iter_1_20250218/_home_lt_ReNewPoNe_framework_save_baseline_iter_1_20250218_iter_12414_merge_hf/critique/result_02_19_15_45_47.jsonl
ultracm_iter_0=/home/lt/ReNewPoNe/eval/CriticBench/src/save_framework/ultracm_iter_0/_home_lt_ReNewPoNe_framework_save_ultracm_iter_0_20250218_iter_6960_merge_hf/critique/result_02_19_15_24_10.jsonl
autoj_with_baseline_data_iter_0=/home/lt/ReNewPoNe/eval/CriticBench/src/save_framework/autoj_with_baseline_data_iter_0/_home_lt_ReNewPoNe_framework_save_autoj_with_baseline_data_iter_0_iter_2939_merge_hf/critique/result_02_19_16_39_45.jsonl
files=($autoj_with_baseline_data_iter_0)
labels=(autoj_with_baseline_data_iter_0)

for index in $(seq 0 0)
do
    file=${files[$index]}
    label=${labels[$index]}
    python evaluate.py  \
        --available_gpus 5 \
        --hf_critic_model $model \
        --tasks Q \
        --prompt_type zs-crit-cot \
        --enable_code_execution \
        --existed_crit_file $file > log/framework_$label.txt
done

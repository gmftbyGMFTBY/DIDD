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

files=($code $exam_question $general_communication $summarization $creative_writing $functional_writing $rewriting)
labels=(code exam_question general_communication summarization creative_writing functional_writing rewriting)

for index in $(seq 0 6)
do
    file=${files[$index]}
    label=${labels[$index]}
    python evaluate.py  \
        --available_gpus 5 \
        --hf_critic_model $model \
        --tasks Q \
        --prompt_type zs-crit-cot \
        --enable_code_execution \
        --existed_crit_file $file > log/domain_analysis_$label.txt
done

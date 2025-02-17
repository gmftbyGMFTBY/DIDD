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

files=($baseline_autoj)
labels=(baseline_autoj)

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
        --existed_crit_file $file > log/$label.txt
done

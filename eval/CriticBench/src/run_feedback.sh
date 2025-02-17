#!/bin/bash

##### response quality
low=/home/lt/ReNewPoNe/response_quality/save_v2/low/iter_7840_merge_hf
medium=/home/lt/ReNewPoNe/response_quality/save_v3/medium/iter_5214_merge_hf
high=/home/lt/ReNewPoNe/response_quality/save_v2/high/iter_7582_merge_hf
overall_response_quality=/home/lt/ReNewPoNe/response_quality/save_v2/overall/iter_10450_merge_hf
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

##### repsonse quality analysis
medium_v4=/home/lt/ReNewPoNe/response_quality/save_v4/medium_v4/iter_10356_merge_hf
overall_v3=/home/lt/ReNewPoNe/response_quality/save_v4/overall_v3/iter_10350_merge_hf
overall_v4=/home/lt/ReNewPoNe/response_quality/save_v4/overall_v4/iter_10330_merge_hf

models=($medium_v4 $overall_v3 $overall_v4)
labels=(medium_v4 overall_v3 overall_v4)

for index in $(seq 0 2)
do
    model=${models[$index]}
    label=${labels[$index]}
    index=$(($index+5))
    echo "Infer $model with $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=$index python evaluate.py --available_gpus $index --tasks Q --hf_critic_model $model --prompt_type zs-crit-cot --enable_code_execution --output_dir response_quality_analysis/$label &
done


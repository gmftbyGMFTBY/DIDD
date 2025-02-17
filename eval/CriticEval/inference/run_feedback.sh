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

models=($code $exam_question $general_communication $summarization $creative_writing $functional_writing $rewriting)
labels=(code exam_question general_communication summarization creative_writing functional_writing rewriting)

for index in $(seq 0 6)
do
    model=${models[$index]}
    label=${labels[$index]}
    index=$(($index+1))
    echo "Inference $model on GPU[$index]; save into save/$label"
    CUDA_VISIBLE_DEVICES=$index python feedback_models.py --model_name $model --output_dir save_domain_analysis/$label --split test &
done

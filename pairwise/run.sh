#!/bin/bash


easy=scripts/easy.py
hard_1=scripts/hard_1.py
hard_2=scripts/hard_2.py
overall=scripts/overall.py
overall_dis=scripts/overall_dis.py
baseline_comp_num_5000=scripts/baseline_comp_num_5000.py
llama3_8b_overall=scripts/llama3_8b_baseline.py


##### hard2 rate exp
hard2_rate_01=scripts/hard_2_rate_exp_0.1.py
hard2_rate_02=scripts/hard_2_rate_exp_0.2.py
hard2_rate_03=scripts/hard_2_rate_exp_0.3.py
hard2_rate_04=scripts/hard_2_rate_exp_0.4.py
hard2_rate_05=scripts/hard_2_rate_exp_0.5.py
hard2_rate_06=scripts/hard_2_rate_exp_0.6.py
hard2_rate_07=scripts/hard_2_rate_exp_0.7.py
hard2_rate_08=scripts/hard_2_rate_exp_0.8.py
hard2_rate_09=scripts/hard_2_rate_exp_0.9.py


###### domain pairwise
nlp_tasks=scripts/nlp_tasks.py
code=scripts/code.py
general_communication=scripts/general_communication.py
exam_question=scripts/exam_question.py
functional_writing=scripts/functional_writing.py
rewriting=scripts/rewriting.py
creative_writing=scripts/creative_writing.py
summarization=scripts/summarization.py

cfg_files=($rewriting $creative_writing $summarization)
labels=(rewriting creative_writing summarization)

cfg_files=($hard2_rate_01 $hard2_rate_02 $hard2_rate_03 $hard2_rate_04 $hard2_rate_05 $hard2_rate_06 $hard2_rate_07)
labels=(hard2_rate_01 hard2_rate_02 hard2_rate_03 hard2_rate_04 hard2_rate_05 hard2_rate_06 hard2_rate_07)


###### revision 20250715
cfg_files=(scripts/qwen2_5_0_5b_baseline.py scripts/qwen2_5_1_5b_baseline.py scripts/qwen2_5_3b_baseline.py scripts/qwen2_5_7b_baseline.py)
labels=(qwen2_5_0_5b_baseline qwen2_5_1_5b_baseline qwen2_5_3b_baseline qwen2_5_7b_baseline)


for index in $(seq 3 3)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    index=$(($index+3))
    echo "Train $cfg_file with label $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir revision_20250715/$label &
done

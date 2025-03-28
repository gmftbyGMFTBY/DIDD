#!/bin/bash

overall=scripts/overall.py
code=scripts/code.py
summarization=scripts/summarization.py
rewriting=scripts/rewriting.py
creative_writing=scripts/creative_writing.py
functional_writing=scripts/functional_writing.py
exam_question=scripts/exam_question.py
general_communication=scripts/general_communication.py
nlp_tasks=scripts/nlp_tasks.py

domain_strategy_uniform=scripts/domain_strategy_uniform.py
domain_strategy_dis=scripts/domain_strategy_dis.py

autoj_iter_0=scripts/autoj_ours_iter_0.py
overall_strong_4=scripts/overall_strong_4.py
overall_weak_4=scripts/overall_weak_4.py

cfg_files=($overall_weak_4)
labels=(overall_weak_4)


dis=scripts/dis.py
uniform=scripts/uniform.py
cfg_files=($dis $uniform)
labels=(dis uniform)

for index in $(seq 0 1)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    echo "Train $cfg_file with label $label on GPU[$index]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save_20250322/$label &
done

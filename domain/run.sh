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

cfg_files=($code $summarization $rewriting $creating_writing $functional_writing $exam_question $general_communication $nlp_tasks $overall)
labels=(code summarization rewriting creating_writing functional_writing exam_question general_communication nlp_tasks overall)

for index in $(seq 0 6)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    index=$(($index+1))
    echo "Train $cfg_file with label $label on GPU[1]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save_analysis/$label &
done

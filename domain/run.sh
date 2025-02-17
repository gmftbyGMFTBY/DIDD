#!/bin/bash

overall=scripts/overall.py
math_code=scriptsmath_code.py
translation_summarization=scripts/translation_summarization.py
chat_qa=scripts/chat_qa.py

cfg_files=($overall $math_code $translation_summarization $chat_qa)
labels=(overall math_code translation_summarization chat_qa)

for index in $(seq 0 1)
do
    cfg_file=${cfg_files[$index]}
    label=${labels[$index]}
    index=$(($index+0))
    echo "Train $cfg_file with label $label on GPU[1]"
    CUDA_VISIBLE_DEVICES=$index NPROC_PER_NODE=1 xtuner train $cfg_file --work-dir save/$label &
done

#!/bin/bash

internlm2_7b_chat=/home/lt/NewPoNe/model/internlm2-7b-chat
internlm2_iter_0=/home/lt/ReNewPoNe/framework/save/comp_baseline_new_resquality_from_hard_2/iter_2276_merge_hf
internlm2_baseline=/home/lt/ReNewPoNe/pairwise/save/hard_2/iter_2028_merge_hf

llama3_8b_instruct=/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct
autoj_ours=/home/lt/ReNewPoNe/baseline/save/autoj_pairwise/iter_2949_merge_hf
qwen2_7b_instruct=/home/lt/models/Qwen2-7B-Instruct

models=($internlm2_iter_0)
models=(deepseek-v3)

models=(auto-j-13b)
models=(ultracm-13b)

for index in $(seq 0 0)
do
    path=${models[$index]}
    index=$(($index+3))
    echo "[!] inference $path on GPU[$index]"
    ./run_one.sh $path 0,1,6 outputs
done

#!/bin/bash

internlm2_7b_chat=/home/lt/NewPoNe/model/internlm2-7b-chat
llama3_8b_instruct=/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct
qwen2_7b_instruct=/home/lt/models/Qwen2-7B-Instruct

autoj_ours=/home/lt/ReNewPoNe/baseline/save/autoj_pairwise/iter_2949_merge_hf
autojj_ours_iter_0=

internlm2_iter_0=/home/lt/ReNewPoNe/framework/save/comp_baseline_new_resquality_from_hard_2/iter_2276_merge_hf
data_mixture_rate_06_8508_iter_1=/home/lt/ReNewPoNe/framework/save/data_mixture_rate_06_8508_iter_1/iter_1000_merge_hf
internlm2_baseline=/home/lt/ReNewPoNe/pairwise/save/hard_2/iter_2028_merge_hf

comp_data_llama3_base_model=/home/lt/ReNewPoNe/framework/save/comp_data_llama3_8b/iter_1918_merge_hf
llama3_baseline_model=/home/lt/ReNewPoNe/pairwise/save/llama3_8b_overall/iter_2576_merge_hf
models=($llama3_baseline_model)

#####
easy=/home/lt/ReNewPoNe/pairwise/save/easy/iter_1284_merge_hf
hard_1=/home/lt/ReNewPoNe/pairwise/save/hard_1/iter_3616_merge_hf
hard_2=/home/lt/ReNewPoNe/pairwise/save/hard_2/iter_2028_merge_hf
models=($easy $hard_1 $hard_2)

comp_data_llama3_on_internlm=/home/lt/ReNewPoNe/framework/save/comp_data_llama3_on_interlm/iter_1958_merge_hf
models=($comp_data_llama3_on_internlm)

comp_iter_0=/home/lt/ReNewPoNe/framework/save/comp_iter_0_only/iter_1958_merge_hf
comp_iter_01=/home/lt/ReNewPoNe/framework/save/comp_iter_01_only/iter_3928_merge_hf
comp_iter_012=/home/lt/ReNewPoNe/framework/save/comp_iter_012_only/iter_5890_merge_hf
comp_iter_0_v2=/home/lt/ReNewPoNe/framework/save/comp_iter_0_v2_only/iter_1620_merge_hf
comp_iter_01_v2=/home/lt/ReNewPoNe/framework/save/comp_iter_01_v2_only/iter_3324_merge_hf
comp_iter_012_v2=/home/lt/ReNewPoNe/framework/save/comp_iter_012_v2_only/iter_4708_merge_hf
models=($comp_iter_012_v2)

for index in $(seq 0 0)
do
    path=${models[$index]}
    index=$(($index+7))
    echo "[!] inference $path on GPU[$index]"
    ./run_one.sh $path $index outputs &
done

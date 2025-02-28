#!/bin/bash

internlm2_7b_chat=/home/lt/NewPoNe/model/internlm2-7b-chat
internlm2_iter_0=/home/lt/ReNewPoNe/framework/save/comp_baseline_new_resquality_from_hard_2/iter_2276_merge_hf
internlm2_baseline=/home/lt/ReNewPoNe/pairwise/save/hard_2/iter_2028_merge_hf

llama3_8b_instruct=/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct
qwen2_7b_instruct=/home/lt/models/Qwen2-7B-Instruct
models=($internlm2_7b_chat $llama3_8b_instruct $qwen2_7b_instruct $internlm2_iter_0 $internlm2_baseline)

comp_data_llama3_base_model=/home/lt/ReNewPoNe/framework/save/comp_data_llama3_8b/iter_1918_merge_hf
llama3_baseline_model=/home/lt/ReNewPoNe/pairwise/save/llama3_8b_overall/iter_2576_merge_hf
llama3_ours=/home/lt/ReNewPoNe/framework/save/comp_llama3_iter_0/iter_6110_merge_hf

autoj_ours=/home/lt/ReNewPoNe/baseline/save/autoj_pairwise/iter_2949_merge_hf
autoj_ours_iter_0=autoj_ours_iter_0=/home/lt/ReNewPoNe/framework/save/comp_autoj_iter_0/iter_6314_merge_hf/

### comp iter 0
comp_iter_exp_0_only=/home/lt/ReNewPoNe/framework/save/comp_iter_0_only/iter_1958_merge_hf

#models=($llama3_ours $autoj_ours $autoj_ours_iter $autoj_ours_iter_0)
models=($comp_iter_exp_0_only)
labels=(comp_iter_exp_0_only)
comp_data_llama3_on_internlm=/home/lt/ReNewPoNe/framework/save/comp_data_llama3_on_interlm/iter_1958_merge_hf
models=($comp_data_llama3_on_internlm)

for index in $(seq 0 0)
do
    path=${models[$index]}
    index=$(($index+1))
    echo "[!] inference $path on GPU[$index]"
    ./run_one.sh $path $index outputs &
done

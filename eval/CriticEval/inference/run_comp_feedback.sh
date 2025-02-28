#!/bin/bash


easy=/home/lt/ReNewPoNe/pairwise/save/easy/iter_1284_merge_hf
hard_1=/home/lt/ReNewPoNe/pairwise/save/hard_1/iter_3616_merge_hf
hard_2=/home/lt/ReNewPoNe/pairwise/save/hard_2/iter_2028_merge_hf
overall_dis=/home/lt/ReNewPoNe/pairwise/save/overall_dis/iter_3552_merge_hf
comp_baseline_iter_0=/home/lt/ReNewPoNe/framework/save/comp_baseline_iter_0/iter_5286_merge_hf
comp_baseline_iter_0_v2=/home/lt/ReNewPoNe/framework/save/comp_baseline_iter_0_v2/iter_10016_merge_hf

autoj_pairwise=/home/lt/ReNewPoNe/baseline/save/autoj_pairwise/iter_2949_merge_hf
llama3_8b_pairwise=/home/lt/ReNewPoNe/pairwise/save/llama3_8b_overall/iter_2576_merge_hf
models=($llama3_8b_pairwise)
labels=(llama3_8b_pairwise)

internlm2=/home/lt/NewPoNe/model/internlm2-7b-chat
llama3=/home/lt/models--meta-llama--Meta-Llama-3-8B-Instruct
qwen=/home/lt/models/Qwen2-7B-Instruct

comp_baseline_new_resquality_from_hard_2=/home/lt/ReNewPoNe/framework/save/comp_baseline_new_resquality_from_hard_2/iter_2276_merge_hf
llama3_comp_baseline_new_resquality_from_hard_2=/home/lt/ReNewPoNe/framework/save/llama3_8b_new_comp/iter_2284_merge_hf


###### comp baseline test num
comp_baseline_test_num_100=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_100/iter_1373_merge_hf
comp_baseline_test_num_200=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_200/iter_2161_merge_hf
comp_baseline_test_num_300=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_300/iter_2485_merge_hf
comp_baseline_test_num_400=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_400/iter_3174_merge_hf
comp_baseline_test_num_500=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_500/iter_3885_merge_hf
comp_baseline_test_num_600=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_600/iter_4483_merge_hf
comp_baseline_test_num_1000=/home/lt/ReNewPoNe/framework/save/baseline_comp_test_num_1000/iter_7051_merge_hf

####

models=($comp_baseline_test_num_100 $comp_baseline_test_num_200 $comp_baseline_test_num_300 $comp_baseline_test_num_400 $comp_baseline_test_num_500 $comp_baseline_test_num_600 $comp_baseline_test_num_1000)
labels=(comp_baseline_test_num_100 comp_baseline_test_num_200 comp_baseline_test_num_300 comp_baseline_test_num_400 comp_baseline_test_num_500 comp_baseline_test_num_600 comp_baseline_test_num_1000)

models=($llama3_comp_baseline_new_resquality_from_hard_2)
labels=(llama3_comp_baseline_new_resquality_from_hard_2)

hard2_rate_01=/home/lt/ReNewPoNe/pairwise/save/hard2_rate_01/iter_2128_merge_hf
hard2_rate_02=/home/lt/ReNewPoNe/pairwise/save/hard2_rate_02/iter_2132_merge_hf
hard2_rate_03=/home/lt/ReNewPoNe/pairwise/save/hard2_rate_03/iter_2084_merge_hf
hard2_rate_04=/home/lt/ReNewPoNe/pairwise/save/hard2_rate_04/iter_2112_merge_hf
hard2_rate_05=/home/lt/ReNewPoNe/pairwise/save/hard2_rate_05/iter_2084_merge_hf
hard2_rate_06=/home/lt/ReNewPoNe/pairwise/save/hard2_rate_06/iter_2060_merge_hf
hard2_rate_07=/home/lt/ReNewPoNe/pairwise/save/hard2_rate_07/iter_2016_merge_hf

####
llama3_8b_new=/home/lt/ReNewPoNe/framework/save/llama3_8b_0225_balance/iter_2956_merge_hf
data_mixture_rate_06_8508_iter_1=/home/lt/ReNewPoNe/framework/save/data_mixture_rate_06_8508_iter_1/iter_1000_merge_hf

models=($data_mixture_rate_06_8508_iter_1)
labels=(data_mixture_rate_06_8508_iter_1)

#### comp_data_llama3_base_Model
comp_data_llama3_base_model=/home/lt/ReNewPoNe/framework/save/comp_data_llama3_8b/iter_1918_merge_hf
models=($comp_data_llama3_base_model)
labels=(comp_data_llama3_base_model)

comp_data_llama3_on_internlm=/home/lt/ReNewPoNe/framework/save/comp_data_llama3_on_interlm/iter_1958_merge_hf

#### comp iter exp
comp_iter_exp_0_only=/home/lt/ReNewPoNe/framework/save/comp_iter_0_only/iter_1958_merge_hf
comp_iter_exp_01_only=/home/lt/ReNewPoNe/framework/save/comp_iter_01_only/iter_3928_merge_hf
comp_iter_exp_012_only=/home/lt/ReNewPoNe/framework/save/comp_iter_012_only/iter_5890_merge_hf
comp_iter_exp_0_v2_only=/home/lt/ReNewPoNe/framework/save/comp_iter_0_v2_only/iter_1620_merge_hf
comp_iter_exp_01_v2_only=/home/lt/ReNewPoNe/framework/save/comp_iter_01_v2_only/iter_3324_merge_hf
comp_iter_exp_012_v2_only=/home/lt/ReNewPoNe/framework/save/comp_iter_012_v2_only/iter_4708_merge_hf
models=($comp_iter_exp_012_v2_only)
labels=(comp_iter_exp_012_v2_only)

for index in $(seq 0 0)
do
    model=${models[$index]}
    label=${labels[$index]}
    index=$(($index+2))
    echo "Inference $model on GPU[$index]; save into save/$label"
    CUDA_VISIBLE_DEVICES=$index python comp_feedback_models.py --model_name $model --output_dir save_comp/$label --split dev &
    CUDA_VISIBLE_DEVICES=$(($index+1)) python comp_feedback_models.py --model_name $model --output_dir save_comp/$label --split test &
done

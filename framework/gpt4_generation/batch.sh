#!/bin/bash

#### paramters
root_path=data_autoj
iter_num=0
gen_num=5
few_shot_num=3
model_path=/home/lt/ReNewPoNe/baseline/save/autoj_ours/iter_3840_merge_hf
model_bsz=32
cuda_gpu_index=7
train_num_each=50
topk=50 # 50 * 50 = 2500

# 1. generate test set
# generate file: {root_path}/iter_{iter_num}/test_set_gn_{gen_num}_fsn_{few_shot_num}
./run_test_set_construction.sh $root_path $iter_num $gen_num $few_shot_num

# 2. evaluate
# generate file: {root_path}/iter_{iter_num}/model_prediction.json
./run_evaluate.sh $root_path $iter_num $gen_num $few_shot_num $model_path $model_bsz $cuda_gpu_index

# 3. prediciton
# generate file: {root_path}/iter_{iter_num}/meta_evaluation.json
./run_meta_evaluate.sh $root_path $iter_num $gen_num $few_shot_num $model_path

# 4. get the distribution file
# generate failure dis file: {root_path}/iter_{iter_num}/top-{topk}-failure-dis.json
./run_stat.sh $root_path $iter_num $topk

# 4. generate train set
failure_dis_file=${root_path}/iter_${iter_num}/top-${topk}-failure-dis.json
# generate file: {root_path}/iter_{iter_num}/train_set_gn_{train_num_each}_fsn_{few_shot_num}.json
./run_train_set_construction.sh $root_path $iter_num $train_num_each $few_shot_num $failure_dis_file

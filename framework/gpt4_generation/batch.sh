#!/bin/bash

#### baseline
# 1. max response quality exp model
# 2. max domain exp model
# 3. random model baseline (random sampleing)
# 4. autoj/ultracm
# 5. 测试迭代几轮的效果（选一个上述表现最好的模型继续刷）

#### paramters
#root_path=data_ultracm_20250218
root_path=data_baseline_20250218_reverse
iter_num=0
test_query_num=100
gen_num=5
few_shot_num=3
#model_path=/home/lt/ReNewPoNe/baseline/save/autoj_ours/iter_3840_merge_hf
model_path=/home/lt/ReNewPoNe/framework/save/baseline/iter_5650_merge_hf
#model_path=/home/lt/ReNewPoNe/framework/save/baseline_20250218/iter_9608_merge_hf
#model_path=/home/lt/ReNewPoNe/baseline/save/ultracm_ours/iter_3980_merge_hf
model_bsz=32
cuda_gpu_index=1
# 最好是设置一个 max 一个 min，那个 domain-quality 表现差，这部分的 train-num-each 比例就要大，否则就要少一些
# 还有设置一个 trainset 数据总量，按照错误比例进行归一化计算每个 domain-quality 的训练数据占比
train_num_each=10
train_query_num=100 # 100 * 20 = 2000
mode=mixture
mixture_rate=0.6 # the mixture weight of new distribution

# 1. generate test set
# generate file: {root_path}/iter_{iter_num}/test_set_gn_{gen_num}_fsn_{few_shot_num}
#./run_test_set_construction.sh $root_path $iter_num $gen_num $few_shot_num $test_query_num

# 2. evaluate
# generate file: {root_path}/iter_{iter_num}/model_prediction.json
#./run_evaluate.sh $root_path $iter_num $gen_num $few_shot_num $model_path $model_bsz $cuda_gpu_index $test_query_num

# 3. prediciton
# generate file: {root_path}/iter_{iter_num}/meta_evaluation.json
#./run_meta_evaluate.sh $root_path $iter_num $gen_num $few_shot_num $model_path

# 4. get the distribution file
# generate failure dis file: {root_path}/iter_{iter_num}/top-{topk}-failure-dis.json
./run_stat.sh $root_path $iter_num $mode $mixture_rate

# 4. generate train set
#failure_dis_file=${root_path}/iter_${iter_num}/${mode}-failure-dis-${mixture_rate}.json
# generate file: {root_path}/iter_{iter_num}/train_set_gn_{train_num_each}_fsn_{few_shot_num}_mode_{mode}.json
#./run_train_set_construction.sh $root_path $iter_num $train_num_each $few_shot_num $failure_dis_file $train_query_num $mode $mixture_rate

#!/bin/bash

# models=(api_model)
# models=(claude-instant-1)
models=(gpt-4-1106-preview)
# models=(gpt-3.5-turbo)
# models=(internlm2-7b-chat)
versions=(1 2)
for model in ${models[@]}
do
    for version in ${versions[@]}
    do
        CUDA_VISIBLE_DEVICES=0 python meta_feedback_models.py \
            --model_name $model \
            --output_dir output_meta_feedback_new_$version \
            --split dev \
            --version $version
    done
done

#!/bin/bash

path=$1
gpu_index=$2
output_folder=$3
echo "Evaluate model $path on GPU [$gpu_index]"
CUDA_VISIBLE_DEVICES=$gpu_index python inference.py --model_name $path --output_dir $output_folder 

#!/bin/bash




model=$v4_model_320_train_no_reference_mathcode
python parse_feedback_outputs.py --model_name $model --output_dir 20240501_320_parsed_feedback_train_no_reference_mathcode --gen_feedback_data_dir 20240501_320_output_feedback_train_no_reference_mathcode --split test
python parse_feedback_outputs.py --model_name $model --output_dir 20240501_320_parsed_feedback_train_no_reference_mathcode --gen_feedback_data_dir 20240501_320_output_feedback_train_no_reference_mathcode --split dev

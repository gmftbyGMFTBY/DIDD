#!/bin/bash

echo "mode: $1"    # feedback, correction, comp_feedback, meta_feedback
echo "format: $2"    # sub, obj
echo "set: $3"    # test, dev
echo "save results into: $4"    # any name for saving the evaluation results
if [ $1 == 'feedback' ];
then
    if [ $2 == "obj" ]; 
    then  
        echo "Inference Objective Evaluation for Feedback Critique Task"
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_framework/baseline" --batch_size 16 --split $3 --obj True 
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_framework/baseline_iter_0" --batch_size 16 --split $3 --obj True 
        python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_framework/baseline_iter_0_v2" --batch_size 16 --split $3 --obj True 
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_v2/overall" --batch_size 16 --split $3 --obj True 
        #exit
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_v2/low" --batch_size 16 --split $3 --obj True 
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_v3/medium" --batch_size 16 --split $3 --obj True 
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_v2/high" --batch_size 16 --split $3 --obj True 
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_v2/medium" --batch_size 16 --split $3 --obj True 
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_v2/overall" --batch_size 16 --split $3 --obj True 
    else
        echo "Inference Subjective Evaluation for Feedback Critique Task"
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_v2/low" --evaluation_dir "./response_quality" --batch_size 16 --split $3 --obj False
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_v3/medium" --evaluation_dir "./response_quality" --batch_size 16 --split $3 --obj False &
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_v2/high" --evaluation_dir "./response_quality" --batch_size 16 --split $3 --obj False &
        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_v2/overall" --evaluation_dir "./response_quality" --batch_size 16 --split $3 --obj False &

        #python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_framework/baseline" --evaluation_dir "./framework" --batch_size 16 --split $3 --obj False &
        python run_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_framework/baseline_iter_0_v2" --evaluation_dir "./framework" --batch_size 16 --split $3 --obj False
    fi
elif [ $1 == 'correction' ];
then
    if [ $2 == "obj" ]; 
    then  
        echo "Inference Objective Evaluation for Correction Critique Task"
        python run_correction.py --root_dir "../data/CriticBench" --prediction_dir "../inference/gpt-4-1106-preview/" --batch_size 16 --split $3 --obj True
	exit
        python run_correction.py --root_dir "../data/CriticBench" --prediction_dir "../inference/relabel_20240901_rlhf_dev_output_correction_by_internlm2-20b-chat_reverse_feedback_new/" --batch_size 16 --split dev --obj True --allow_models _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_385_epoch_2_0701_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_385_hf_ckpt > 1_.txt
        python run_correction.py --root_dir "../data/CriticBench" --prediction_dir "../inference/relabel_20240901_rlhf_dev_output_correction_by_internlm2-7b-chat_reverse_feedback_new/" --batch_size 16 --split dev --obj True --allow_models _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_385_epoch_2_0701_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_385_hf_ckpt > 2_.txt
        python run_correction.py --root_dir "../data/CriticBench" --prediction_dir "../inference/relabel_20240901_rlhf_dev_output_correction_by_s2_add_critictuning_reverse_feedback_new/" --batch_size 16 --split dev --obj True --allow_models _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_385_epoch_2_0701_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_385_hf_ckpt > 3_.txt
        python run_correction.py --root_dir "../data/CriticBench" --prediction_dir "../inference/relabel_20240901_rlhf_dev_output_correction_by_llama-3-70b-instruct_reverse_feedback_new/" --batch_size 16 --split dev --obj True --allow_models _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_385_epoch_2_0701_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_385_hf_ckpt > 4_.txt
        python run_correction.py --root_dir "../data/CriticBench" --prediction_dir "../inference/relabel_20240901_rlhf_dev_output_correction_by_mixtral-8x7b-instruct_reverse_feedback_new/" --batch_size 16 --split dev --obj True --allow_models _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_385_epoch_2_0701_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_385_hf_ckpt > 5_.txt
    else
        echo "Inference Subjective Evaluation for Correction Critique Task"
        #python run_correction.py --root_dir "../data/CriticBench" --prediction_dir "../inference/test_output_correction_by_s2_add_critictuning" --evaluation_dir "20240704_resumm_correction_evaluation_cache_test" --batch_size 32 --split test --obj False --allow_models _cpfs02_llm_shared_public_lantian_exp_20240501_sft_7b_critique_autoj_26_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_critic_autoj_26_hf_ckpt _cpfs02_llm_shared_public_lantian_exp_20240501_sft_7b_critique_ultracm_878_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_critic_ultracm_878_hf_ckpt _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_385_epoch_2_0701_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_385_hf_ckpt internlm2-7b-chat themis
        
        ### no-ref, no-criteria, no-task, no-all, ours
        #python run_correction.py --root_dir "../data/CriticBench" --prediction_dir "../inference/relabel_20240901_rlhf_dev_output_correction_by_llama-3-70b-instruct_reverse_feedback" --evaluation_dir "20240905_sft_ablation_study_correction_evaluation_with_feedback_llama_3_70b_no_feedback_reverse_feedback" --batch_size 32 --split dev --obj False --allow_models _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_385_epoch_2_0701_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_385_hf_ckpt _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_no_criteria_275_epoch_2_0703_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_no_criteria_275_hf_ckpt
        python run_correction.py --root_dir "../data/CriticBench" --prediction_dir "../inference/relabel_20240901_rlhf_dev_output_correction_by_llama-3-70b-instruct_reverse_feedback_new" --evaluation_dir "20240905_sft_ablation_study_correction_evaluation_with_feedback_llama_3_70b_no_feedback_reverse_feedback_new" --batch_size 32 --split dev --obj False  --allow_models _cpfs02_llm_shared_public_lantian_exp_promethues_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_promethues_540_hf
        
        #_cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_no_ref_333_epoch_2_0703_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_no_ref_333_hf_ckpt _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_no_task_376_epoch_2_0703_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_no_task_376_hf_ckpt _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_no_all_215_epoch_2_0703_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_no_all_215_hf_ckpt_cpfs02_llm_shared_public_lantian_exp_metacritique_step_train_exp_claude_feedback_step_400_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_claude_feedback_400_hf_ckpt _cpfs02_llm_shared_public_lantian_exp_metacritique_step_train_exp_qwen_feedback_step_400_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_qwen_feedback_400_hf_ckpt _cpfs02_llm_shared_public_lantian_exp_metacritique_step_train_exp_internlm2_feedback_step_400_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_internlm_feedback_400_hf_ckpt_cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_385_epoch_2_0701_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_385_hf_ckpt _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_no_all_215_epoch_2_0703_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_no_all_215_hf_ckpt _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_no_criteria_275_epoch_2_0703_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_no_criteria_275_hf_ckpt _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_no_ref_333_epoch_2_0703_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_no_ref_333_hf_ckpt _cpfs02_llm_shared_public_lantian_exp_20240618_sft_7b_critique_nips2024_d4_st_5_l1_resumm_no_task_376_epoch_2_0703_aliyun_Ampere_7B_v1.1_enchance_FT_v1.0.0_s1_rc47_FINAL_critic_v4_st_5_l1_resumm_no_task_376_hf_ckpt
    fi
elif [ $1 == 'comp_feedback' ];
then
    if [ $2 == "obj" ]; 
    then  
        echo "Inference Objective Evaluation for Comparison-based Feedback Critique Task"
        python run_comp_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/save_comp/overall" --batch_size 16 --split $3 --obj True
    else
        echo "Inference Subjective Evaluation for Comparison-based Feedback Critique Task"
        python run_comp_feedback.py --root_dir "../data/criticbench_v1.3" --prediction_dir "../example_data/prediction_v1.3" --evaluation_dir "../example_data/evaluation_v1.3/" --batch_size 1 --split $3 --obj False
    fi
elif [ $1 == 'meta_feedback' ];
then
    echo "Inference Objective Evaluation for Meta-Feedback Critique Task"
    python run_meta_feedback.py --root_dir "../data/CriticBench" --prediction_dir "../inference/" --batch_size 32 --split $3 --obj True
fi

1. response quality
* medium_v4, overall_v3 (0.25, 0.5, 0.25), overall_v4 (0.2, 0.6, 0.2)

2. domain
* analysis_*
* overall

2025-2-26

##### 使用其他模型的生成分佈來訓練模型

1. baselne
2. other-model: llama3-8b
3. baseline_20250218_iter_0_mixture_0.6 (internlm2-7b-chat + baseline + 生成數據)

##### iter exp
../framework/gpt4_generation/batch_iter_1.sh

##### pairwise針對llama3模型


#### InternLM2-7B-Chat数据给 Llama3-8B-Instruct
1. singlewise: data/baseline_iter_0.json
2. pairwise: data/comp_baseline_iter_0_v2.json

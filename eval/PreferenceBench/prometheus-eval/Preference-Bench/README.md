---
dataset_info:
  features:
  - name: orig_criteria
    dtype: string
  - name: orig_feedback_A
    dtype: string
  - name: orig_feedback_B
    dtype: string
  - name: orig_instruction
    dtype: string
  - name: orig_reference_answer
    dtype: string
  - name: orig_response_A
    dtype: string
  - name: orig_response_B
    dtype: string
  - name: orig_score_A
    dtype: string
  - name: orig_score_B
    dtype: string
  - name: orig_preference
    dtype: string
  - name: instruction
    dtype: string
  - name: output
    dtype: string
  - name: input
    dtype: string
  - name: orig_feedback
    dtype: string
  - name: messages
    list:
    - name: content
      dtype: string
    - name: role
      dtype: string
  - name: __index_level_0__
    dtype: int64
  splits:
  - name: train
    num_bytes: 43873852
    num_examples: 1998
  download_size: 0
  dataset_size: 43873852
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
---
# Dataset Card for "Promixtheus-Relative-Bench"

[More Information needed](https://github.com/huggingface/datasets/blob/main/CONTRIBUTING.md#how-to-contribute-to-the-dataset-cards)
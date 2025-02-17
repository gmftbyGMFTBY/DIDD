export HOME=/cpfs01/user/lantain/
source /cpfs01/user/lantian/configuration/.bashrc
conda activate py39
python -c "import socket; print(socket.gethostbyname(socket.gethostname()))"  # 查看节点ip
echo "========== llama3 8B at =========="

CUDA_VISIBLE_DEVICES=0 lmdeploy serve api_server /cpfs01/shared/public/public_hdd/llmeval/model_weights/hf_hub/models--meta-llama--Meta-Llama-3-8B-Instruct/snapshots/1448453bdb895762499deb4176c1dd83b145fac1 --server-name 0.0.0.0 --server-port 2333 --tp 1 --max-batch-size 4

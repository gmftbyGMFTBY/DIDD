export HOME=/cpfs01/user/lantain/
source /cpfs01/user/lantian/configuration/.bashrc
conda activate py39
python -c "import socket; print(socket.gethostbyname(socket.gethostname()))"  # 查看节点ip
echo "========== llama3 8B at =========="

CUDA_VISIBLE_DEVICES=0,1,2,3 lmdeploy serve api_server /cpfs01/shared/public/public_hdd/llmeval/model_weights/hf_hub/models--meta-llama--Meta-Llama-3-70B-Instruct/snapshots/5fcb2901844dde3111159f24205b71c25900ffbd --server-name 0.0.0.0 --server-port 2333 --tp 4 --max-batch-size 1

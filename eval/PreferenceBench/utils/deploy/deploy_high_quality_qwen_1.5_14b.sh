export HOME=/cpfs01/user/lantain/
source /cpfs01/user/lantian/configuration/.bashrc
conda activate py39
python -c "import socket; print(socket.gethostbyname(socket.gethostname()))"  # 查看节点ip
echo "========== Qwen1.5 14B at =========="

CUDA_VISIBLE_DEVICES=0 lmdeploy serve api_server /cpfs01/shared/public/public_hdd/llmeval/model_weights/hf_hub/models--Qwen--Qwen1.5-14B-Chat/snapshots/519cfcc93dc11a4f470138d800b4987484e70677  --server-name 0.0.0.0 --server-port 2333 --tp 1 --max-batch-size 4

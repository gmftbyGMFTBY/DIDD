export HOME=/cpfs01/user/lantain/
source /cpfs01/user/lantian/configuration/.bashrc
conda activate py39
python -c "import socket; print(socket.gethostbyname(socket.gethostname()))"  # 查看节点ip
echo "========== Qwen1.5 72B at =========="

CUDA_VISIBLE_DEVICES=0,1,2,3 lmdeploy serve api_server /cpfs01/shared/public/public_hdd/llmeval/model_weights/hf_hub/models--Qwen--Qwen1.5-72B-Chat/snapshots/96a2df029f0045547ee55cfc8b925b2cac4353e5  --server-name 0.0.0.0 --server-port 2333 --tp 4 --max-batch-size 1

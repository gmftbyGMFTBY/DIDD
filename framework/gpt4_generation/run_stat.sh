#!/bin/bash

echo "[!] generate state file"
echo "[!] root-path: $1"
echo "[!] iter-num: $2"
echo "[!] topk: $3"
python stat.py --topk $3 --root-path $1 --iter-num $2

#!/bin/bash

echo "[!] generate state file"
echo "[!] root-path: $1"
echo "[!] iter-num: $2"
echo "[!] mode: $3"
#python stat.py --root-path $1 --iter-num $2 --mode $3 --mixture-rate $4 --reverse 1
python stat.py --root-path $1 --iter-num $2 --mode $3 --mixture-rate $4 --reverse 0

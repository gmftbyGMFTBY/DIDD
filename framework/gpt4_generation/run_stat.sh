#!/bin/bash

echo "[!] generate state file"
echo "[!] root-path: $1"
echo "[!] iter-num: $2"
python stat.py --root-path $1 --iter-num $2

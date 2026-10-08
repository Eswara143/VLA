#!/usr/bin/env bash
# Unitree G1 Dex3 ToastedBread Dataset Downloader (Bash)
# Repository: https://huggingface.co/datasets/unitreerobotics/G1_Dex3_ToastedBread_Dataset

set -e

DEST_DIR="./G1_Dex3_ToastedBread_Dataset"
BASE_URL="https://huggingface.co/datasets/unitreerobotics/G1_Dex3_ToastedBread_Dataset/resolve/main"

echo "=========================================================="
echo " Unitree G1 Dex3 ToastedBread Dataset Downloader (Shell)"
echo " Total files: 38 | Total size: ~13.83 GB"
echo " Destination: $DEST_DIR"
echo "=========================================================="

mkdir -p "$DEST_DIR"

# Method selection
echo "Select download method:"
echo " 1) aria2c (Fastest, multi-connection resume)"
echo " 2) python script (download_dataset.py)"
echo " 3) curl (built-in standard)"
echo " 4) huggingface-cli (official HF tool)"
echo " 5) git clone with lfs"

read -p "Enter choice [1-5] (default 2): " choice
choice=${choice:-2}

case $choice in
  1)
    if ! command -v aria2c &> /dev/null; then
      echo "aria2c not found. Installing via apt or falling back..."
      sudo apt-get install -y aria2 || true
    fi
    echo "Creating download URL list..."
    python3 -c "
import json
with open('dataset_files.json') as f:
    files = json.load(f)
with open('aria2_input.txt', 'w') as out:
    for item in files:
        out.write(item['download_url'] + '\n')
        out.write(f\"  dir=$DEST_DIR/\" + '/'.join(item['path'].split('/')[:-1]) + '\n')
        out.write(f\"  out=\" + item['path'].split('/')[-1] + '\n')
"
    aria2c -i aria2_input.txt -j 4 -x 8 -k 1M -c
    ;;
  2)
    python3 download_dataset.py --dest "$DEST_DIR" --type all
    ;;
  3)
    python3 -c "
import json, subprocess, os
with open('dataset_files.json') as f:
    files = json.load(f)
for f in files:
    dest = os.path.join('$DEST_DIR', f['path'])
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    print(f'Downloading {f[\"path\"]}...')
    subprocess.run(['curl', '-C', '-', '-L', '-o', dest, f['download_url']])
"
    ;;
  4)
    pip install -U "huggingface_hub[cli]"
    huggingface-cli download unitreerobotics/G1_Dex3_ToastedBread_Dataset --repo-type dataset --local-dir "$DEST_DIR"
    ;;
  5)
    git clone https://huggingface.co/datasets/unitreerobotics/G1_Dex3_ToastedBread_Dataset "$DEST_DIR"
    ;;
  *)
    echo "Invalid option."
    exit 1
    ;;
esac

echo "Download completed!"

#!/usr/bin/env python3
"""
Unitree G1 Dex3 ToastedBread Dataset Downloader
Dataset: https://huggingface.co/datasets/unitreerobotics/G1_Dex3_ToastedBread_Dataset
Total Size: ~13.83 GB (38 files)
"""

import os
import sys
import argparse
import urllib.request
import time
from pathlib import Path

DATASET_ID = "unitreerobotics/G1_Dex3_ToastedBread_Dataset"
BASE_URL = f"https://huggingface.co/datasets/{DATASET_ID}/resolve/main"

# Complete file listing with sizes in bytes
FILES = [
    {"path": ".gitattributes", "size": 1564, "category": "doc"},
    {"path": "README.md", "size": 6534, "category": "doc"},
    {"path": "meta/info.json", "size": 6592, "category": "meta"},
    {"path": "meta/stats.json", "size": 13915, "category": "meta"},
    {"path": "meta/tasks.parquet", "size": 4771, "category": "meta"},
    {"path": "meta/episodes/chunk-000/file-000.parquet", "size": 932470, "category": "meta"},
    {"path": "data/chunk-000/file-000.parquet", "size": 73190848, "category": "data"},
    {"path": "data/chunk-000/file-001.parquet", "size": 4878512, "category": "data"},
    {"path": "videos/observation.images.cam_left_high/chunk-000/file-000.mp4", "size": 522969329, "category": "video_cam_left_high"},
    {"path": "videos/observation.images.cam_left_high/chunk-000/file-001.mp4", "size": 517720235, "category": "video_cam_left_high"},
    {"path": "videos/observation.images.cam_left_high/chunk-000/file-002.mp4", "size": 513876932, "category": "video_cam_left_high"},
    {"path": "videos/observation.images.cam_left_high/chunk-000/file-003.mp4", "size": 518069678, "category": "video_cam_left_high"},
    {"path": "videos/observation.images.cam_left_high/chunk-000/file-004.mp4", "size": 519069320, "category": "video_cam_left_high"},
    {"path": "videos/observation.images.cam_left_high/chunk-000/file-005.mp4", "size": 519849310, "category": "video_cam_left_high"},
    {"path": "videos/observation.images.cam_left_high/chunk-000/file-006.mp4", "size": 517578204, "category": "video_cam_left_high"},
    {"path": "videos/observation.images.cam_left_high/chunk-000/file-007.mp4", "size": 522437632, "category": "video_cam_left_high"},
    {"path": "videos/observation.images.cam_left_high/chunk-000/file-008.mp4", "size": 270889216, "category": "video_cam_left_high"},
    {"path": "videos/observation.images.cam_left_wrist/chunk-000/file-000.mp4", "size": 517454848, "category": "video_cam_left_wrist"},
    {"path": "videos/observation.images.cam_left_wrist/chunk-000/file-001.mp4", "size": 516515840, "category": "video_cam_left_wrist"},
    {"path": "videos/observation.images.cam_left_wrist/chunk-000/file-002.mp4", "size": 521261056, "category": "video_cam_left_wrist"},
    {"path": "videos/observation.images.cam_left_wrist/chunk-000/file-003.mp4", "size": 518678528, "category": "video_cam_left_wrist"},
    {"path": "videos/observation.images.cam_left_wrist/chunk-000/file-004.mp4", "size": 523419648, "category": "video_cam_left_wrist"},
    {"path": "videos/observation.images.cam_left_wrist/chunk-000/file-005.mp4", "size": 192088064, "category": "video_cam_left_wrist"},
    {"path": "videos/observation.images.cam_right_high/chunk-000/file-000.mp4", "size": 516708352, "category": "video_cam_right_high"},
    {"path": "videos/observation.images.cam_right_high/chunk-000/file-001.mp4", "size": 519487488, "category": "video_cam_right_high"},
    {"path": "videos/observation.images.cam_right_high/chunk-000/file-002.mp4", "size": 514207744, "category": "video_cam_right_high"},
    {"path": "videos/observation.images.cam_right_high/chunk-000/file-003.mp4", "size": 516773888, "category": "video_cam_right_high"},
    {"path": "videos/observation.images.cam_right_high/chunk-000/file-004.mp4", "size": 523206656, "category": "video_cam_right_high"},
    {"path": "videos/observation.images.cam_right_high/chunk-000/file-005.mp4", "size": 519630848, "category": "video_cam_right_high"},
    {"path": "videos/observation.images.cam_right_high/chunk-000/file-006.mp4", "size": 509435904, "category": "video_cam_right_high"},
    {"path": "videos/observation.images.cam_right_high/chunk-000/file-007.mp4", "size": 523886592, "category": "video_cam_right_high"},
    {"path": "videos/observation.images.cam_right_high/chunk-000/file-008.mp4", "size": 311353344, "category": "video_cam_right_high"},
    {"path": "videos/observation.images.cam_right_wrist/chunk-000/file-000.mp4", "size": 521361408, "category": "video_cam_right_wrist"},
    {"path": "videos/observation.images.cam_right_wrist/chunk-000/file-001.mp4", "size": 524132352, "category": "video_cam_right_wrist"},
    {"path": "videos/observation.images.cam_right_wrist/chunk-000/file-002.mp4", "size": 521445376, "category": "video_cam_right_wrist"},
    {"path": "videos/observation.images.cam_right_wrist/chunk-000/file-003.mp4", "size": 514246656, "category": "video_cam_right_wrist"},
    {"path": "videos/observation.images.cam_right_wrist/chunk-000/file-004.mp4", "size": 507062272, "category": "video_cam_right_wrist"},
    {"path": "videos/observation.images.cam_right_wrist/chunk-000/file-005.mp4", "size": 513298432, "category": "video_cam_right_wrist"},
]

def format_size(bytes_num):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_num < 1024:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024
    return f"{bytes_num:.2f} TB"

def download_file(file_info, dest_dir, resume=True):
    path = file_info["path"]
    expected_size = file_info["size"]
    dest_path = dest_dir / path
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    url = f"{BASE_URL}/{path}"
    headers = {"User-Agent": "UnitreeDownloader/1.0"}

    downloaded = 0
    if resume and dest_path.exists():
        downloaded = dest_path.stat().st_size
        if downloaded >= expected_size:
            print(f"  [ALREADY DONE] {path} ({format_size(downloaded)})")
            return True
        headers["Range"] = f"bytes={downloaded}-"
        print(f"  [RESUMING] {path} from {format_size(downloaded)} / {format_size(expected_size)}")
    else:
        print(f"  [DOWNLOADING] {path} ({format_size(expected_size)})")

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            mode = "ab" if downloaded > 0 else "wb"
            with open(dest_path, mode) as f:
                start_time = time.time()
                last_print = start_time
                chunk_size = 1024 * 1024 # 1MB chunks
                
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    
                    now = time.time()
                    if now - last_print > 1.0 or downloaded == expected_size:
                        percent = (downloaded / expected_size) * 100 if expected_size > 0 else 100
                        speed = (downloaded / (now - start_time + 0.001)) / (1024 * 1024)
                        print(f"\r    -> {percent:5.1f}% | {format_size(downloaded)} / {format_size(expected_size)} | {speed:5.1f} MB/s", end="", flush=True)
                        last_print = now
        print()
        return True
    except Exception as e:
        print(f"\n  [ERROR] Failed to download {path}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Download Unitree G1 Dex3 Toasted Bread Dataset")
    parser.add_argument("--dest", default="./G1_Dex3_ToastedBread_Dataset", help="Destination folder (default: ./G1_Dex3_ToastedBread_Dataset)")
    parser.add_argument("--type", choices=["all", "data-only", "meta-only", "videos-only", "cam-high", "cam-wrist"], default="all",
                        help="Choose category: 'all' (13.8GB), 'data-only' (Parquet only ~78MB), 'meta-only' (JSON/episodes ~1MB), 'videos-only' (All MP4s), 'cam-high', 'cam-wrist'")
    parser.add_argument("--dry-run", action="store_true", help="List files to be downloaded without actually downloading")
    args = parser.parse_args()

    target_files = []
    for f in FILES:
        cat = f["category"]
        if args.type == "all":
            target_files.append(f)
        elif args.type == "data-only" and cat in ["data", "meta", "doc"]:
            target_files.append(f)
        elif args.type == "meta-only" and cat in ["meta", "doc"]:
            target_files.append(f)
        elif args.type == "videos-only" and "video" in cat:
            target_files.append(f)
        elif args.type == "cam-high" and ("cam_left_high" in cat or "cam_right_high" in cat):
            target_files.append(f)
        elif args.type == "cam-wrist" and ("cam_left_wrist" in cat or "cam_right_wrist" in cat):
            target_files.append(f)

    total_bytes = sum(f["size"] for f in target_files)
    dest_path = Path(args.dest).resolve()

    print("=" * 70)
    print(" Unitree G1 Dex3 ToastedBread Dataset Downloader")
    print("=" * 70)
    print(f" Target Directory : {dest_path}")
    print(f" Selected Filter  : {args.type}")
    print(f" Total Files      : {len(target_files)}")
    print(f" Total Size       : {format_size(total_bytes)}")
    print("=" * 70)

    if args.dry_run:
        print("Dry run listing:")
        for idx, f in enumerate(target_files, 1):
            print(f"  {idx:2d}. {f['path']} ({format_size(f['size'])})")
        return

    print("Starting download...\n")
    success_count = 0
    for idx, f in enumerate(target_files, 1):
        print(f"[{idx}/{len(target_files)}] Processing {f['path']}...")
        if download_file(f, dest_path):
            success_count += 1

    print("\n" + "=" * 70)
    print(f" Finished: {success_count}/{len(target_files)} files downloaded successfully.")
    print(f" Location: {dest_path}")
    print("=" * 70)

if __name__ == "__main__":
    main()

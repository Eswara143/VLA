#!/usr/bin/env python3
"""
Build the website data from the datasets/ folder.

Every datasets/*.json file is one dataset card. This script validates them,
fills in anything left out, and writes categorized_datasets.json and data.js,
which are the two files the website reads.

Usage:
    python3 scripts/build_data.py          # rebuild
    python3 scripts/build_data.py --check  # validate only, write nothing
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = ROOT / "datasets"
OUT_JSON = ROOT / "categorized_datasets.json"
OUT_JS = ROOT / "data.js"

# Hand name as it appears in a dataset name -> (finger_category, finger_label, hand_type)
HANDS = {
    "Dex1": ("2_fingers", "2 Fingers (Dex1)", "Dex1 Two-Fingered Parallel Gripper"),
    "Dex3": ("3_fingers", "3 Fingers (Dex3)", "Dex3 Three-Fingered Dexterous Hand"),
    "Brainco": ("5_fingers", "5 Fingers (Brainco)", "Brainco Five-Fingered Anthropomorphic Hand"),
    "Inspire": ("5_fingers", "5 Fingers (Inspire)", "Inspire Five-Fingered Dexterous Hand"),
}
CATEGORY_DEFAULTS = {
    "2_fingers": ("2 Fingers", "Two-Fingered Gripper"),
    "3_fingers": ("3 Fingers", "Three-Fingered Hand"),
    "5_fingers": ("5 Fingers", "Five-Fingered Hand"),
}
CATEGORY_ORDER = ["2_fingers", "3_fingers", "5_fingers"]
# Name parts that are not part of the task description
NON_TASK_PARTS = {"G1", "H1", "Z1", "Dual", "WBT", "Dataset"} | set(HANDS)
HF_URL = re.compile(r"^https://huggingface\.co/datasets/([^/?#]+/[^/?#]+)/?$")
# The site puts id and url straight into HTML attributes, so keep them plain.
SAFE_TEXT = re.compile(r"^[^\s'\"<>`\\]+$")


class DatasetError(Exception):
    pass


def find_hand(name):
    for part in name.split("_"):
        if part in HANDS:
            return part
    return None


def normalize(entry, source):
    if not isinstance(entry, dict):
        raise DatasetError(f"{source}: file must contain one JSON object {{...}}")

    name = entry.get("name")
    url = entry.get("url")
    if not isinstance(name, str) or not name.strip():
        raise DatasetError(f'{source}: "name" is required')
    if not isinstance(url, str) or not url.startswith("https://"):
        raise DatasetError(f'{source}: "url" is required and must start with https://')
    name = name.strip()

    hf = HF_URL.match(url)
    dataset_id = entry.get("id") or (hf.group(1) if hf else name)
    for field, value in (("name", name), ("id", dataset_id), ("url", url)):
        if not isinstance(value, str) or not SAFE_TEXT.match(value):
            raise DatasetError(f'{source}: "{field}" must not contain spaces, quotes or < > characters')

    hand = find_hand(name)
    category = entry.get("finger_category") or (HANDS[hand][0] if hand else None)
    if category not in CATEGORY_ORDER:
        raise DatasetError(
            f'{source}: cannot tell the hand type from the name "{name}". '
            f'Add "finger_category": "2_fingers", "3_fingers" or "5_fingers" to the file.'
        )
    if hand and HANDS[hand][0] == category:
        default_label, default_hand_type = HANDS[hand][1], HANDS[hand][2]
    else:
        default_label, default_hand_type = CATEGORY_DEFAULTS[category]

    task_parts = [p for p in name.split("_") if p not in NON_TASK_PARTS]
    default_task = " ".join(task_parts) or name

    downloads = entry.get("downloads", 0)
    likes = entry.get("likes", 0)
    tags = entry.get("tags", [])
    for field, value in (("downloads", downloads), ("likes", likes)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise DatasetError(f'{source}: "{field}" must be a whole number')
    if not isinstance(tags, list) or not all(isinstance(t, str) for t in tags):
        raise DatasetError(f'{source}: "tags" must be a list of text values')

    return {
        "id": dataset_id,
        "name": name,
        "downloads": downloads,
        "likes": likes,
        "tags": tags,
        "url": url,
        "finger_category": category,
        "finger_label": str(entry.get("finger_label") or default_label),
        "hand_type": str(entry.get("hand_type") or default_hand_type),
        "task_name": str(entry.get("task_name") or default_task),
    }


def load_all():
    files = sorted(DATASETS_DIR.glob("*.json"))
    if not files:
        raise DatasetError(f"no dataset files found in {DATASETS_DIR}")

    datasets, errors, seen = [], [], {}
    for path in files:
        source = f"datasets/{path.name}"
        try:
            try:
                entry = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as e:
                raise DatasetError(f"{source}: not valid JSON ({e})")
            item = normalize(entry, source)
            if item["id"] in seen:
                raise DatasetError(f'{source}: same dataset as {seen[item["id"]]} ("{item["id"]}")')
            seen[item["id"]] = source
            datasets.append(item)
        except DatasetError as e:
            errors.append(str(e))

    if errors:
        raise DatasetError("\n".join(errors))

    datasets.sort(key=lambda d: (CATEGORY_ORDER.index(d["finger_category"]), -d["downloads"], d["name"]))
    return datasets


def main():
    check_only = "--check" in sys.argv[1:]
    try:
        datasets = load_all()
    except DatasetError as e:
        print("Dataset files have problems:\n" + str(e), file=sys.stderr)
        return 1

    counts = {c: sum(1 for d in datasets if d["finger_category"] == c) for c in CATEGORY_ORDER}
    summary = ", ".join(f"{c}: {n}" for c, n in counts.items())
    print(f"{len(datasets)} datasets OK ({summary})")

    if not check_only:
        body = json.dumps(datasets, indent=2, ensure_ascii=False)
        OUT_JSON.write_text(body, encoding="utf-8")
        OUT_JS.write_text(f"window.CATEGORIZED_DATASETS = {body};\n", encoding="utf-8")
        print(f"Wrote {OUT_JSON.name} and {OUT_JS.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
import sys
import json
import os

# Read matrix JSON from stdin
matrix = json.load(sys.stdin)

# Ensure assets directory exists

os.makedirs("assets", exist_ok=True)

# Write header and rows
with open("assets/IMAGES.md", "w") as f:
    f.write("| Python | Variant | Mode | Base Image | Tags |\n")
    f.write("|--------|---------|------|------------|------|\n")
    for entry in matrix:
        tag = f"ghcr.io/{os.environ['GITHUB_REPOSITORY']}:py{entry['python']}-{entry['extra']}-{entry['mode']}"
        f.write(
            f"| {entry['python']} | {entry['extra']} | {entry['mode']} | {entry['base']} | {tag} |\n"
        )

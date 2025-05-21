#!/usr/bin/env python3
import sys
import json
import yaml

# Load matrix.yaml
with open(".github/matrix.yaml") as f:
    cfg = yaml.safe_load(f)

matrix = [
    {"python": p, "extra": e, "mode": m, "base": cfg["base_map"][e]}
    for p in cfg["python"]
    for e in cfg["extra"]
    for m in cfg["mode"]
]

# Emit JSON to stdout
print(json.dumps(matrix))

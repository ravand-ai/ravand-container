#!/usr/bin/env python3


README = "README.md"
TABLE = "assets/IMAGES.md"
START = "<!-- IMAGES_TABLE_START -->"
END = "<!-- IMAGES_TABLE_END -->"

# Load README
text = open(README).read().splitlines()

# Load table (just the lines starting with '|')
table_lines = [l for l in open(TABLE) if l.startswith("|")]

out = []
inside = False
for line in text:
    if START in line:
        out.append(line)
        out.extend(table_lines)
        inside = True
        continue
    if END in line:
        out.append(line)
        inside = False
        continue
    if not inside:
        out.append(line)

# Write back
with open(README, "w") as f:
    f.write("\n".join(out) + "\n")

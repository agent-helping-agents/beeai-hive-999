#!/usr/bin/env python3
"""
Calculates SHA256 entropy of each vault file and rotates if below threshold.
"""
import hashlib, os, sys
vault = os.getenv("VAULT_PATH")
for fname in os.listdir(vault):
    path = os.path.join(vault, fname)
    with open(path, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    print(f"{fname}: {h}")
# TODO: Rotate if age > threshold

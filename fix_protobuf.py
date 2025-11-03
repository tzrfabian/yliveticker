#!/usr/bin/env python3
"""Fix protobuf version compatibility issue"""

import subprocess
import sys

print("Downgrading protobuf to compatible version...")
try:
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'protobuf<3.21'], check=True)
    print("Successfully downgraded protobuf!")
    print("\nYou can now run:")
    print("  python yliveticker/client_code.py")
except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    sys.exit(1)


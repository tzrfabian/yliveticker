#!/usr/bin/env python3
"""Regenerate protobuf file from .proto source"""

import subprocess
import sys
import os

# Check if protoc is available
try:
    result = subprocess.run(['protoc', '--version'], capture_output=True, text=True)
    print(f"Found protoc: {result.stdout.strip()}")
except FileNotFoundError:
    print("protoc not found. Trying to install grpcio-tools...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'grpcio-tools'], check=True)
    # After installing grpcio-tools, try to find protoc
    import shutil
    protoc_path = shutil.which('protoc')
    if not protoc_path:
        # Try using the protoc from grpcio_tools
        import grpc_tools.protoc
        print("Using grpc_tools.protoc to regenerate...")
        # We'll handle this differently
        protoc_path = None
    else:
        print(f"Found protoc at: {protoc_path}")

# Generate the protobuf file
proto_file = 'yliveticker/yaticker.proto'
output_dir = 'yliveticker'

try:
    # Try using protoc directly
    subprocess.run([
        'protoc',
        '--python_out=.',
        '--proto_path=yliveticker',
        proto_file
    ], check=True)
    print(f"Successfully regenerated {output_dir}/yaticker_pb2.py")
except (FileNotFoundError, subprocess.CalledProcessError):
    # Fallback: try using grpc_tools
    try:
        from grpc_tools import protoc
        protoc.main([
            'grpc_tools.protoc',
            '--python_out=.',
            '--proto_path=yliveticker',
            proto_file
        ])
        print(f"Successfully regenerated {output_dir}/yaticker_pb2.py using grpc_tools")
    except Exception as e:
        print(f"Error: {e}")
        print("\nPlease install protoc manually:")
        print("  Option 1: Install Protocol Buffers compiler from https://grpc.io/docs/protoc-installation/")
        print("  Option 2: Install grpcio-tools: pip install grpcio-tools")
        print("  Option 3: Downgrade protobuf: pip install 'protobuf<3.21'")
        sys.exit(1)


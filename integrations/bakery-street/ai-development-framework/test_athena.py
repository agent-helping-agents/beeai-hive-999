#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, '/home/booze/ai-development/aws-env/lib/python3.11/site-packages')

from aws_athena_client import AthenaClient

# Test Athena connection
athena = AthenaClient()
print("✅ AWS Athena client ready")
print(f"Account: {os.getenv("AWS_ACCOUNT_ID", "YOUR_ACCOUNT_ID")}")
print(f"User: {os.getenv("AWS_USER", "YOUR_USERNAME")}")
print(f"S3 Output: {athena.s3_output}")
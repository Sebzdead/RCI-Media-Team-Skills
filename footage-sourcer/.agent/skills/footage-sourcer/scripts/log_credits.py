#!/usr/bin/env python3
import sys
import os
import datetime

def append_to_manifest(source_name, url, license_type):
    """
    Appends discovered footage data directly to an ongoing manifest 
    for the video editors to drop into YouTube descriptions.
    """
    manifest_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../credits_manifest.txt"))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_line = f"[{timestamp}] SOURCE: {source_name} | URL: {url} | LICENSE: {license_type}\n"
    
    try:
        with open(manifest_path, "a", encoding="utf-8") as f:
            f.write(log_line)
        print(f"SUCCESS: Logged {source_name} to local manifest tracking file.")
    except Exception as e:
        print(f"ERROR: Failed writing to log file: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 log_credits.py [Source] [URL] [License]", file=sys.stderr)
        sys.exit(1)
    append_to_manifest(sys.argv[1], sys.argv[2], sys.argv[3])

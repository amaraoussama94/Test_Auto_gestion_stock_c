"""
@file utils/version.py
@brief Extracts version information from git commit messages.
@details This script retrieves the version number from the last 10 git commit messages.
@note The version is expected to be in the format [vvX.Y] where X and Y are integers.dd
"""
import subprocess
import re

def extract_version_from_git():
    try:
        result = subprocess.run(
            ["git", "log", "--pretty=format:%s", "-n", "10"],
            capture_output=True,
            text=True,
            check=True
        )
        for line in result.stdout.splitlines():
            match = re.search(r"\[vv\d+\.\d+\]", line)
            if match:
                return match.group(0).strip("[]")
    except subprocess.CalledProcessError as e:
        print("Git log failed:", e)
    return "vv_unknown"

if __name__ == '__main__':
    print("Detected version:", extract_version_from_git())

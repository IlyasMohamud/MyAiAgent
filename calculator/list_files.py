import os
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', '.venv')]
    for f in sorted(files):
        p = os.path.join(root, f)
        print(f"{os.path.getsize(p):>8}  {p}")
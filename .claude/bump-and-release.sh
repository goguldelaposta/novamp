#!/bin/bash
# Bump patch version, commit, tag, and push — fires automatically after each Claude task.
cd /Users/andrei/NovaMP

# Nothing to do if the working tree is clean
if [ -z "$(git status --porcelain 2>/dev/null)" ]; then
  exit 0
fi

# Compute next patch version from package.json
CURRENT=$(python3 -c "import json; print(json.load(open('package.json'))['version'])")
IFS='.' read -r MAJ MIN PAT <<< "$CURRENT"
NEW="$MAJ.$MIN.$((PAT + 1))"

# Update "version" field in both files — regex preserves all other formatting
VERSION="$NEW" python3 -c "
import os, re
v = os.environ['VERSION']
for path in ['package.json', 'src-tauri/tauri.conf.json']:
    with open(path) as f:
        txt = f.read()
    txt = re.sub(
        r'(\"version\"\s*:\s*)\"[^\"]+\"',
        lambda m: m.group(1) + f'\"{v}\"',
        txt, count=1
    )
    with open(path, 'w') as f:
        f.write(txt)
"

git add -A
git commit -m "release v$NEW"
git tag "v$NEW"
git push && git push --tags

printf '{"systemMessage": "Released v%s"}\n' "$NEW"

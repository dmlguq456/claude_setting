#!/bin/bash
# g3: clean main — 본작업 요청이 main 트리 직접 작업으로 가면 안 됨
set -eu
WORK=$1
mkdir -p "$WORK/.golden_pre"
git init -q --bare "$WORK/origin.git"
git clone -q "$WORK/origin.git" "$WORK/repo"
cd "$WORK/repo"
git config user.email golden@test && git config user.name golden
git checkout -q -b main
printf 'def main():\n    print("app")\n' > app.py
git add -A && git commit -q -m "init" && git push -q -u origin main
git rev-parse main > "$WORK/.golden_pre/main_sha"

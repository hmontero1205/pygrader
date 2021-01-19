#!/bin/bash

if [ "$#" -lt 1 ]; then
	echo "Usage: $0 <assignment name> [org/repo to clone on setup]" >&2
	exit 1
fi

cd "$(dirname "$0")"

ASS="$(echo "$1" | tr '[:upper:]' '[:lower:]')"
if [ -d "$ASS" ]; then
	read -p "Overwrite '$ASS'? [y/N]: " RESP
	if [ "$RESP" == y ] || [ "$RESP" == Y ]; then
		rm -rf "$ASS"
	else
		exit 1
	fi
fi

mkdir "$ASS" || exit
cp rubric.json.in "$ASS/rubric.json"
cp grader.py.in "$ASS/grader.py"
sed -i "s/ASSIGNMENT/$ASS/g" "$ASS/grader.py"
test "$#" -gt 1 && cp clone_setup.in "$ASS/setup"
touch "$ASS/setup"
chmod +x "$ASS/setup"
sed -i "s~REPO~$2~g" "$ASS/setup"

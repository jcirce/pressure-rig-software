#!/usr/bin/env bash

[[ "$1" == "$2" ]] && echo "Inputs and output are the same!" && exit 1

test -f "$2" && echo "File '$2' exists!" && exit 1

sort -t'_' -k3 -g "$1" | awk '{print $2","$4}' | sed -E 's/(.*)?PSI([0-9]+\.[0-9]+)\.png,([0-9]+\.[0-9]+)/\2,\3/g' > "$2"

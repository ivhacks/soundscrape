#!/bin/bash 

if [ $# -ne 1 ]; then
    echo "Usage: $0 <url>"
    exit 1
fi

python3 view_link.py "$1"
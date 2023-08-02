#!/usr/bin/bash

if [ -t 0 ]; then
    echo "Please provide a filename as input using < symbol."
    exit 1
fi

# Read the content of the file specified as input
input=$(cat)


echo $(python main.py "$input")


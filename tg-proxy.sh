#!/bin/bash

script_dir=$(dirname "$(readlink -f "$0")")

source $script_dir/.venv/bin/activate
python3 $script_dir/src/main.py

#!/usr/bin/env bash

set -e

log_dir="$PWD/logs"
db_dir="$PWD/db"
ilog="$log_dir/install.log"

if [ ! -d "$log_dir" ]; then
    mkdir -p "$log_dir"
fi

if [ ! -d "$db_dir" ]; then
    mkdir -p "$db_dir"
fi

status_check() {
    if [ $? -eq 0 ]; then
        echo -e "$1 - Installed"
    else
        echo -e "$1 - Failed!"
        exit 1
    fi
}

# ...rest of your script

echo -e '\n[+] Log Saved :'"$ilog"


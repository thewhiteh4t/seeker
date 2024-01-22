#!/usr/bin/env bash

LOG_DIR=$PWD/logs
DB_DIR=$PWD/db
ILOG=$LOG_DIR/install.log

mkdir -p $LOG_DIR $DB_DIR

status_check() {
    if [ $? -eq 0 ]
    then
        echo -e "$1 - Installed"
    else
        echo -e "$1 - Failed!"
    fi
}

debian_install() {
    echo -e '=====================\nINSTALLING FOR DEBIAN\n=====================\n' > "$ILOG"

    pkgs="python3 python3-pip python3-requests python3-packaging python3-psutil php"

    install_cmd() {
        echo -ne '$1\r'
        sudo apt -y install $1 &>> "$ILOG"
        status_check $1
        echo -e '\n--------------------\n' >> "$ILOG"
    }

    for pkg_name in $pkgs; do
        install_cmd $pkg_name
    done
}

fedora_install() {
    echo -e '=====================\nINSTALLING FOR FEDORA\n=====================\n' > "$ILOG"

    pkgs="python3 python3-pip python3-requests python3-packaging python3-psutil php"

    install_cmd() {
        echo -ne "$1\r"
        sudo dnf install $1 -y &>> "$ILOG"
        status_check $1
        echo -e '\n--------------------\n' >> "$ILOG"
    }

    for pkg_name in $pkgs; do
        install_cmd $pkg_name
    done
}

termux_install() {
    echo -e '=====================\nINSTALLING FOR TERMUX\n=====================\n' > "$ILOG"

    pkgs="python php"
    pip_pkgs="requests packaging psutil"

    install_cmd() {
        echo -ne "$1\r"
        apt -y install $1 &>> "$ILOG"
        status_check $1
        echo -e '\n--------------------\n' >> "$ILOG"
    }

    install_pip() {
        echo -ne "$1\r"
        pip install -U $1 &>> "$ILOG"
        status_check $1
        echo -e '\n--------------------\n' >> "$ILOG"
    }

    for pkg_name in $pkgs; do
        install_cmd $pkg_name
    done

    for pkg_name in $pip_pkgs; do
        install_pip $pkg_name
    done
}

arch_install() {
    echo -e '=========================\nINSTALLING FOR ARCH LINUX\n=========================\n' > "$ILOG"

    install_cmd() {
        echo -ne "$1\r"
        yes | sudo pacman -S $1 --needed &>> "$ILOG"
        status_check $1
        echo -e '\n--------------------\n' >> "$ILOG"
    }

    pkgs="python3 python-pip python-requests python-packaging python-psutil php"

    for pkg_name in $pkgs; do
        install_cmd $pkg_name
    done
}

echo -e '[!] Installing Dependencies...\n'

if [ -f '/etc/arch-release' ]; then
    arch_install
elif [ -f '/etc/fedora-release' ]; then
    fedora_install
else
    if [ -z "${TERMUX_VERSION}" ]; then
        debian_install
    else
        termux_install
    fi
fi

echo -e '=========\nCOMPLETED\n=========\n' >> "$ILOG"

echo -e '\n[+] Log Saved :' "$ILOG"

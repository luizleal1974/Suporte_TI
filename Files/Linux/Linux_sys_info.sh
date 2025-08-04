#!/bin/bash

## System information

echo ""
echo "Software (operating system)"
echo "Kernel $(uname -r | cut -d'-' -f1)"
echo "Ubuntu $(uname -v | grep -oE '[0-9]{2}\.[0-9]{2}') LTS"
echo "$(lsb_release -d | cut -f2-)"
echo "$(gnome-shell --version)"
echo ""
echo "Hardware"
echo "$(sudo dmidecode | grep -A3 '^System Information')"
echo "$(fastfetch -s host --logo none)"
echo "$(fastfetch -s cpu --logo none) ($(grep 'model name' /proc/cpuinfo | head -1 | grep -o '[0-9.]\+GHz' | sed 's/GHz/ GHz/'))"
echo "$(fastfetch -s gpu --logo none)"
echo ""
echo "Developed by Luiz Henrique Leal"
echo ""


#!/bin/bash

## Linux System Information Requirements

## Atualizar sistema (Apps e Sistema Operacional)
os_update(){
sudo apt update
sudo apt upgrade -y
}

## Instalar pacotes do Python
python_prog(){
sudo apt install python3-pip -y
pip install matplotlib
pip install psutil
sudo apt install python3-tk -y
}

## Fastfetch: informacoes sobre a maquina.
pc_info(){
sudo add-apt-repository ppa:zhangsongcui3371/fastfetch
sudo apt update
sudo apt install fastfetch
}

## Executar shell script
os_update
python_prog
pc_info

## Mensagem
echo "REQUISITOS INSTALADOS"


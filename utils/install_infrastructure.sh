#!/usr/bin/bash

# Função para instalar dependências no Debian/Ubuntu
install_debian() {
    echo "Detectado Debian/Ubuntu."
    sudo apt update
    sudo apt install -y meson libevent-dev libjson-c-dev make git curl  gzip wget clang

}

# Função para instalar dependências no Fedora
install_fedora() {
    echo "Detectado Fedora."
    sudo dnf install -y meson libevent-devel json-c-devel make git curl gzip wget clang
}

# Função para instalar dependências no Arch
install_arch() {
    echo "Detectado Arch."
    sudo pacman -Syu --noconfirm meson libevent json-c make git curl gzip wget clang
}

install_centos() {
    echo "Detectado Cent oS."
    sudo yum install -y meson libevent-devel json-c-devel make git curl gzip wget clang
}

# Detectando a distribuição
if [ -f /etc/os-release ]; then
    . /etc/os-release
    case "$ID" in
        debian)
            install_debian
            ;;
        ubuntu)
            install_debian
            ;;
        fedora)
            install_fedora
            ;;
        arch)
            install_arch
            ;;
        centos)
            install_centos
            ;;
        *)
            echo "Distribuição não suportada: $ID"
            exit 1
            ;;
    esac
else
    echo "Não foi possível detectar a distribuição."
    exit 1
fi

# Criando diretorio de trabalho
echo "Criando diretório de trabalho..."

mkdir -p /eda

cd /eda

# clonando repositorio
echo "Clonando repositórios..."

git clone --recursive https://github.com/LSC-Unicamp/processor-ci-controller
git clone https://github.com/LSC-Unicamp/processor-ci
git clone --recursive https://github.com/LSC-Unicamp/processor-ci-tests

# Instalando OSS-CAD-Suite
echo "Instalando OSS-CAD-Suite..."

cd /eda

wget https://github.com/YosysHQ/oss-cad-suite-build/releases/download/2024-10-03/oss-cad-suite-linux-x64-20241003.tgz

tar -xvzf oss-cad-suite-linux-x64-20241003.tgz
rm oss-cad-suite-linux-x64-20241003.tgz

curl -sSL https://raw.githubusercontent.com/lushaylabs/openfpgaloader-ubuntufix/main/setup.sh | sh

# Instalando RISCV-TOOLCHAIN
echo "Instalando RISCV-TOOLCHAIN..."

cd /eda

git clone --recursive https://github.com/riscv-collab/riscv-gnu-toolchain.git

cd riscv-gnu-toolchain

mkdir -p /eda/riscv

./configure --prefix=/eda/riscv

make -j$(nproc)

echo "Instalação concluída com sucesso!"

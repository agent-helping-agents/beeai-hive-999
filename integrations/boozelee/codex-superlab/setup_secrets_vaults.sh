#!/bin/bash
set -e

sudo apt-get update
sudo apt-get install -y git-crypt

wget https://releases.hashicorp.com/vault/1.14.0/vault_1.14.0_linux_amd64.zip
unzip vault_1.14.0_linux_amd64.zip
chmod +x vault
sudo mv vault /usr/local/bin/
rm vault_1.14.0_linux_amd64.zip

nohup vault server -dev > ~/codex-superlab/vault.log 2>&1 &

npm install -g @bitwarden/cli

mkdir -p ~/api-keys
chmod 700 ~/api-keys

ln -sf ~/api-keys ~/Desktop/API_Vault

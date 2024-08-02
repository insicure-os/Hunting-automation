#!/bin/bash

# Update package list and install dependencies
sudo apt update
sudo apt install -y git cmake python3-pip

# Install Go if not already installed
if ! command -v go &> /dev/null; then
    sudo apt install -y golang-go
fi

# Create a directory for the tools
mkdir -p /root/tools

# bbscope
echo "Installing bbscope..."
go install github.com/sw33tLie/bbscope@latest

# subfinder
echo "Installing subfinder..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# nuclei
echo "Installing nuclei..."
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# httpx
echo "Installing httpx..."
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# katana
echo "Installing katana..."
go install github.com/projectdiscovery/katana/cmd/katana@latest

# dirsearch
echo "Installing dirsearch..."
git clone https://github.com/maurosoria/dirsearch /root/tools/dirsearch
cd /root/tools/dirsearch
pip3 install -r requirements.txt
python3 setup.py install

# gf
echo "Installing gf..."
go install github.com/tomnomnom/gf@latest

# bxss
echo "Installing bxss..."
go install github.com/ethicalhackingplayground/bxss.git

# paramspider
echo "Installing paramspider..."
git clone https://github.com/devanshbatham/paramspider /root/tools/paramspider
cd /root/tools/paramspider
pip3 install .

# corsy
echo "Installing corsy..."
pip3 install requests
git clone https://github.com/s0md3v/Corsy /root/tools/Corsy
cd /root/tools/Corsy
pip3 install -r requirements.txt

# gau
echo "Installing gau..."
go install github.com/lc/gau/v2/cmd/gau@latest

# urldedupe
echo "Installing urldedupe..."
git clone https://github.com/ameenmaali/urldedupe.git /root/tools/urldedupe
cd /root/tools/urldedupe
cmake .
make

# naabu
echo "Installing naabu..."
go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest

# dalfox
echo "Installing dalfox..."
go install github.com/hahwul/dalfox/v2@latest

# Copy binaries to /usr/bin
echo "Copying binaries to /usr/bin..."
sudo cp /root/go/bin/* /usr/bin/
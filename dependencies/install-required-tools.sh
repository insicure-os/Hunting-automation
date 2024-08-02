#!/bin/bash

# Update package list and install dependencies
sudo apt update
sudo apt install -y git cmake python3-pip

# Install Go if not already installed
if ! command -v go &> /dev/null; then
    sudo apt install -y golang-go
fi

# Create a directory for the tools under the current user's home directory
TOOLS_DIR=$HOME/tools
mkdir -p $TOOLS_DIR

# bbscope
if ! command -v bbscope &> /dev/null; then
    echo "Installing bbscope..."
    go install github.com/sw33tLie/bbscope@latest
else
    echo "bbscope is already installed"
fi

# subfinder
if ! command -v subfinder &> /dev/null; then
    echo "Installing subfinder..."
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
else
    echo "subfinder is already installed"
fi

# nuclei
if ! command -v nuclei &> /dev/null; then
    echo "Installing nuclei..."
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
else
    echo "nuclei is already installed"
fi

# httpx
if ! command -v httpx &> /dev/null; then
    echo "Installing httpx..."
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
else
    echo "httpx is already installed"
fi

# katana
if ! command -v katana &> /dev/null; then
    echo "Installing katana..."
    go install github.com/projectdiscovery/katana/cmd/katana@latest
else
    echo "katana is already installed"
fi

# gf
if ! command -v gf &> /dev/null; then
    echo "Installing gf..."
    go install github.com/tomnomnom/gf@latest
else
    echo "gf is already installed"
fi

# bxss
if ! command -v bxss &> /dev/null; then
    echo "Installing bxss..."
    go install github.com/ethicalhackingplayground/bxss.git
else
    echo "bxss is already installed"
fi

# paramspider
if [ ! -d "$HOME/tools/paramspider" ]; then
    echo "Installing paramspider..."
    git clone https://github.com/devanshbatham/paramspider $HOME/tools/paramspider
    cd $HOME/tools/paramspider
    pip3 install .
else
    echo "paramspider is already installed"
fi

# corsy
if [ ! -d "$HOME/tools/Corsy" ]; then
    echo "Installing corsy..."
    pip3 install requests
    git clone https://github.com/s0md3v/Corsy $HOME/tools/Corsy
    cd $HOME/tools/Corsy
    pip3 install -r requirements.txt
else
    echo "corsy is already installed"
fi

# dirsearch
if [ ! -d "$HOME/tools/dirsearch" ]; then
    echo "Installing dirsearch..."
    git clone https://github.com/maurosoria/dirsearch $HOME/tools/dirsearch
    cd $HOME/tools/dirsearch
    pip3 install -r requirements.txt
    python3 setup.py install
else
    echo "dirsearch is already installed"
fi

# gau
if ! command -v gau &> /dev/null; then
    echo "Installing gau..."
    go install github.com/lc/gau/v2/cmd/gau@latest
else
    echo "gau is already installed"
fi

# urldedupe
if [ ! -d "$HOME/tools/urldedupe" ]; then
    echo "Installing urldedupe..."
    git clone https://github.com/ameenmaali/urldedupe.git $HOME/tools/urldedupe
    cd $HOME/tools/urldedupe
    cmake .
    make
else
    echo "urldedupe is already installed"
fi

# naabu
if ! command -v naabu &> /dev/null; then
    echo "Installing naabu..."
    go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
else
    echo "naabu is already installed"
fi

# dalfox
if ! command -v dalfox &> /dev/null; then
    echo "Installing dalfox..."
    go install github.com/hahwul/dalfox/v2@latest
else
    echo "dalfox is already installed"
fi

# Copy binaries to /usr/bin
echo "Copying binaries to /usr/bin..."
sudo cp $HOME/go/bin/ * /usr/bin/

# mv custom sqli tool to desire directory
echo "Moving CustomBsqli to desire directory"
sudo mv customBsqli $HOME/tools
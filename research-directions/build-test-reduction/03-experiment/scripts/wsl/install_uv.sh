set -euo pipefail
mkdir -p ~/bt-lab/dl/uv && cd ~/bt-lab/dl/uv
B=https://github.com/astral-sh/uv/releases/latest/download
curl -sSLO $B/uv-x86_64-unknown-linux-gnu.tar.gz
curl -sSLO $B/uv-x86_64-unknown-linux-gnu.tar.gz.sha256
sha256sum -c uv-x86_64-unknown-linux-gnu.tar.gz.sha256
ls -l uv-x86_64-unknown-linux-gnu.tar.gz
tar xzf uv-x86_64-unknown-linux-gnu.tar.gz
mkdir -p ~/.local/bin && cp uv-x86_64-unknown-linux-gnu/uv uv-x86_64-unknown-linux-gnu/uvx ~/.local/bin/
~/.local/bin/uv --version
~/.local/bin/uv python install 3.12
ls $(dirname $(~/.local/bin/uv python find 3.12))/../include/python3.12/Python.h

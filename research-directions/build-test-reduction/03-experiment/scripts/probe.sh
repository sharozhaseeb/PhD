ls /usr/include/python3.12/Python.h 2>&1
dpkg -l | grep -E "python3.12-(venv|dev)|python3-pip|virtualenv" | awk '{print $2,$3}'
cd ~/bt-lab/exp/repos
echo "--- bottleneck"; git -C bottleneck log -1 --format=%cd 933b653; git -C bottleneck show --stat 0819d3a | tail -3; git -C bottleneck ls-tree -r --name-only 2b9c661 | grep -vE "^doc" | head -40
echo "--- sqlglot bench"; git -C sqlglot ls-tree --name-only HEAD benchmarks/
echo "--- nx bench"; git -C networkx ls-tree -r --name-only HEAD benchmarks/ | head

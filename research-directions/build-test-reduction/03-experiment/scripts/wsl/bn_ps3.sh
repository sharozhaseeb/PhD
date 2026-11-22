ps aux | grep -E 'bn_build38|uv |setup.py|cc1' | grep -v grep | cut -c1-160
ls ~/bt-lab/exp/venvs/bn38/lib/python3.8/site-packages | head

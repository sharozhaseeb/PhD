ls ~/.local/share/uv/python/ 2>&1; ls ~/bn38_build.log 2>&1; ps aux | grep -E 'uv |python|cc1' | grep -v grep | cut -c1-150 | head -5

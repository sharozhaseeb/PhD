cd ~/bt-lab/exp/repos/bottleneck
git merge-base --is-ancestor 52f6cd1 f51ed86 && echo "52f6cd1 IS ancestor of f51ed86"
git merge-base --is-ancestor 52f6cd1 22657ac && echo "52f6cd1 ancestor of 22657ac(old base)" || echo "52f6cd1 NOT ancestor of old base 22657ac"
git merge-base --is-ancestor 52f6cd1 c9168481 && echo yes || echo "NOT ancestor of c9168481"
git show f51ed86:setup.py | grep -n "iterators\|depends" 
git show 52f6cd1 --stat --format='%h %ad %s' --date=short | cat

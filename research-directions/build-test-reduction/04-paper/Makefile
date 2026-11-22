PY ?= python

.PHONY: all check manifest

all:
	$(PY) scripts/make_all.py
	$(PY) scripts/check.py

check:
	$(PY) scripts/check.py

manifest:
	$(PY) scripts/make_all.py --manifest

#!/usr/bin/env bash


pip3 install -U pip setuptools wheel cython
pip install git+https://github.com/Carrene/restfulpy@develop
pip3 install -r requirements-dev.txt
pip3 install -e .

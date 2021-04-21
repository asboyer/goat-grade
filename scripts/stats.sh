#!/usr/bin/env bash

echo Updating standard statistics ...
python3 stats/stats.py
echo Updated!
echo Updating advanced statistics ...
python3 stats/stats2.py
echo Updated!


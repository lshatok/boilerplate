#!/usr/bin/env bash
find /WT -type f -exec sed -i 's/ugly/beautiful/g' {} \;

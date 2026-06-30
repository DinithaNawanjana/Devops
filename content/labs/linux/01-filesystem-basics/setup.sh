#!/bin/sh
# Runs once when the sandbox starts. Clean slate in the home directory.
cd /root || exit 0
rm -rf project
exit 0

#!/bin/bash
set -e
cd /root/app
git -c protocol.file.allow=always submodule add /root/lib.git vendor/lib
git commit -qm "chore: add lib submodule"

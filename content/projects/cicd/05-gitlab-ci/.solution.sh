#!/bin/bash
set -e
mkdir -p /root/repo
cat > /root/repo/.gitlab-ci.yml <<'YML'
stages:
  - build
  - test
build:
  stage: build
  cache:
    paths:
      - .cache/
  script:
    - make build
  artifacts:
    paths:
      - dist/
test:
  stage: test
  script:
    - make test
YML

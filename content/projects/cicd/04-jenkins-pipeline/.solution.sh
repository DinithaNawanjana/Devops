#!/bin/bash
set -e
mkdir -p /root/repo
cat > /root/repo/Jenkinsfile <<'JF'
pipeline {
  agent any
  stages {
    stage('Build')  { steps { sh 'make build' } }
    stage('Test')   { steps { sh 'make test' } }
    stage('Deploy') { steps { sh 'make deploy' } }
  }
}
JF

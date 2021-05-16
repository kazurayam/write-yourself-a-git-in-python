#!/usr/bin/env bash
set -e

function step() {
    pos=$(caller)
    echo $pos $@
}

wyag=$(realpath ./wyag)

testdir=tmp/wyag-tests
if [[ -e $testdir ]]; then
    rm -rf $testdir/*
else
    mkdir $testdir
fi
cd $testdir
step "working on $(pwd)"

step Create repos
$wyag init left
git init right > /dev/null






cd -

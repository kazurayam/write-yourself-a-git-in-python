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

step status
cd left
git status > /dev/null
cd ../right
git status > /dev/null
cd ..

step hash-object
echo "Don't read me" > README
$wyag hash-object README > hash1
git hash-object README > hash2
cmp --quiet hash1 hash2



cd -

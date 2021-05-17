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
git init right > /dev/null 2> /dev/null


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
cmp hash1 hash2


step hash-object -w
cd left
$wyag hash-object -w ../README > /dev/null
cd ../right
git hash-object -w ../README > /dev/null
cd ..
ls left/.git/objects/b1/7df541639ec7814a9ad274e177d9f8da1eb951 > /dev/null
ls right/.git/objects/b1/7df541639ec7814a9ad274e177d9f8da1eb951 > /dev/null


step cat-file
cd left
$wyag cat-file blob b17d > ../file1
cd ../right
git cat-file blob b17d > ../file2
cd ..
cmp file1 file2


step cat-file with long hash
cd left
$wyag cat-file blob b17df541639ec7814a9ad274e177d9f8da1eb951 > ../file1
cd ../right
git cat-file blob b17df541639ec7814a9ad274e177d9f8da1eb951 > ../file2
cd ..
cmp file1 file2


step "Create commit (git only, nothing is testd)"
cd left
echo "Aleph" > hebraic-letter.txt
git add hebraic-letter.txt
GIT_AUTHOR_DATE="2010-01-01 01:02:03" \
    GIT_COMMITTER_DATE="2010-01-01 01:02:03" \
    git commit --no-gpg-sign -m "Initial commit" > /dev/null
cd ../right
echo "Aleph" > hebraic-letter.txt
git add hebraic-letter.txt
GIT_AUTHOR_DATE="2010-01-01 01:02:03" \
    GIT_COMMITTER_DATE="2010-01-01 01:02:03" \
    git commit --no-gpg-sign -m "Initial commit" > /dev/null
cd ..


step cat-file on commit object without indirection
cd left
$wyag cat-file commit HEAD > ../file1
cd ../right
git cat-file commit HEAD > ../file2
cd ..
cmp file1 file2


step cat-file on tree object redirected from commit
cd left
$wyag cat-file tree HEAD > ../file1
cd ../right
git cat-file tree HEAD > ../file2
cd ..
cmp file1 file2


step "Add some directories and commits (git only, nothing is tested)"
cd left
mkdir a
echo "Alpha" > a/greek_letters
mkdir b
echo "Hamza" > a/arabic_letters
git add a/*
GIT_AUTHOR_DATE="2010-01-01 01:02:03" \
               GIT_COMMITTER_DATE="2010-01-01 01:02:03" \
               git commit --no-gpg-sign -m "Commit 2" > /dev/null
cd ..


step ls-tree
cd left
$wyag ls-tree HEAD > ../file1
cd ../right
git ls-tree HEAD > ../file2
cd ..
cmp file1 file2

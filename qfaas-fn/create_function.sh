#!/bin/sh

template=$1
function=$2

faas-cli new --lang $1 $2 --append=./functions.yml --prefix="quantumdev"
sed -i '$d' build.txt

echo $2 >> build.txt
echo "" >> build.txt

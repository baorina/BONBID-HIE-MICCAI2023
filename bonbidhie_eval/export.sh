#!/usr/bin/env bash

./build.sh

docker save bonbidhie2023_eval | gzip -c > bonbidhie2023_eval.tar.gz

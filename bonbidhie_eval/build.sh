#!/usr/bin/env bash
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

docker build -t bonbidhie2023_eval "$SCRIPTPATH"
